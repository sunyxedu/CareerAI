// server.js
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Endpoint to handle AI assessment
app.post('/assess', async (req, res) => {
    const userAnswer = req.body.answer;

    try {
        const response = await axios.post(
            'https://api.openai.com/v1/completions',
            {
                model: 'text-davinci-003',
                prompt: `Assess the following interview answer and provide constructive feedback:\n\nAnswer: "${userAnswer}"\n\nFeedback:`,
                max_tokens: 150,
                temperature: 0.7,
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
                },
            }
        );

        const feedback = response.data.choices[0].text.trim();
        res.json({ feedback });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error assessing the answer.' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});