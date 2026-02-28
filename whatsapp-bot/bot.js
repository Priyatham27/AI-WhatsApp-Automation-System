const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const SERVER_URL = "http://localhost:8000/whatsapp";

// 🛡️ Cooldown tracking (anti-spam)
const userCooldown = {};
const COOLDOWN_TIME = 5000; // 5 seconds

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('📱 Scan this QR code:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('🤖 WhatsApp AI Bot is ready!');
});

client.on('message', async (message) => {

    try {

        // 🔒 Ignore own messages
        if (message.fromMe) return;

        // 🔒 Ignore group messages
        if (message.from.includes('@g.us')) return;

        // 🔒 Ignore status updates
        if (message.from === 'status@broadcast') return;

        // 🔒 Ignore newsletters / channels
        if (message.from.includes('@newsletter')) return;

        // 🔒 Ignore media messages
        if (message.hasMedia) return;

        // 🔒 Ignore empty messages
        if (!message.body || message.body.trim() === "") return;

        // 🛡️ Rate limiting
        const now = Date.now();
        const lastMessageTime = userCooldown[message.from];

        if (lastMessageTime && (now - lastMessageTime < COOLDOWN_TIME)) {
            console.log(`⚠️ Cooldown active for ${message.from}`);
            return;
        }

        userCooldown[message.from] = now;

        console.log(`📩 Incoming from ${message.from}: ${message.body}`);

        const response = await axios.post(
            SERVER_URL,
            {
                Body: message.body,
                Sender: message.from
            },
            { timeout: 20000 }
        );

        const replyText = response.data;

        // 🔒 Avoid empty reply
        if (!replyText || replyText.trim() === "") {
            console.log("⚠️ Empty reply ignored");
            return;
        }

        console.log("🤖 Reply:", replyText);

        // ✅ Safer send (instead of reply quoting)
        await client.sendMessage(message.from, replyText);

    } catch (err) {

        if (err.response) {
            console.error("❌ Backend Error:", err.response.data);
        } else {
            console.error("❌ AI Error:", err.message);
        }
    }
});

client.on('auth_failure', msg => {
    console.error('❌ Authentication failed:', msg);
});

client.on('disconnected', reason => {
    console.log('⚠️ Client disconnected:', reason);
    console.log("🔁 Attempting to reconnect...");
    client.initialize();
});

client.initialize();
