import express from 'express';
import bodyParser from 'body-parser';
import axios from 'axios';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(express.static('public'));

app.post('/api/assess', async (req, res) => {
    if (!process.env.OPENAI_API_KEY) {
        return res.status(500).json({ error: 'OpenAI API key is not configured' });
    }

    const userAnswer = req.body.answer;
    try {
        const response = await axios.post(
            'https://api.openai.com/v1/chat/completions',  // Updated API endpoint
            {
                model: 'gpt-3.5-turbo',  // Updated model
                messages: [{
                    role: 'user',
                    content: `Assess the following interview answer and provide constructive feedback:\n\nAnswer: "${userAnswer}"\n\nFeedback:`
                }],
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
        
        const feedback = response.data.choices[0].message.content.trim();
        res.json({ feedback });
    } catch (error) {
        console.error('OpenAI API Error:', error.response?.data || error.message);
        res.status(500).json({ 
            error: 'Error assessing the answer.',
            details: error.response?.data?.error?.message || error.message
        });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
