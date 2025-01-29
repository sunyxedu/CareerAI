// public/script.js
document.addEventListener('DOMContentLoaded', () => {
    const speechBtn = document.getElementById('speech-btn');
    const listenQuestionBtn = document.getElementById('listen-question-btn');
    const questionContainer = document.getElementById('question-container');
    const questionText = document.getElementById('question');
    const answerTextarea = document.getElementById('answer');
    const submitAnswerBtn = document.getElementById('submit-answer-btn');
    const feedbackContainer = document.getElementById('feedback-container');
    const feedbackText = document.getElementById('feedback');

    let questions = [];
    let currentQuestion = '';

    // Fetch questions from the text file
    fetch('questions.txt')
        .then(response => response.text())
        .then(data => {
            questions = data.split('\n').map(q => q.trim()).filter(q => q.length > 0);
        })
        .catch(err => console.error('Error loading questions:', err));

    // Function to get a random question
    const getRandomQuestion = () => {
        const randomIndex = Math.floor(Math.random() * questions.length);
        return questions[randomIndex];
    };

    // Text-to-Speech for the question
    const speakQuestion = (text) => {
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    };

    // Event listener for Start Interview button
    speechBtn.addEventListener('click', () => {
        currentQuestion = getRandomQuestion();
        questionText.textContent = currentQuestion;
        questionContainer.style.display = 'block';
        feedbackContainer.style.display = 'none';
        answerTextarea.value = '';
        speakQuestion(currentQuestion);
    });

    // Event listener for Listen to Question button
    listenQuestionBtn.addEventListener('click', () => {
        if (currentQuestion) {
            speakQuestion(currentQuestion);
        }
    });

    // Event listener for Submit Answer button
    submitAnswerBtn.addEventListener('click', () => {
        const userAnswer = answerTextarea.value.trim();
        if (userAnswer.length === 0) {
            alert('Please enter your answer before submitting.');
            return;
        }

        // Send the answer to the backend for assessment
        fetch('/assess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answer: userAnswer }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.feedback) {
                feedbackText.textContent = data.feedback;
                feedbackContainer.style.display = 'block';
            } else {
                feedbackText.textContent = 'No feedback received.';
                feedbackContainer.style.display = 'block';
            }
        })
        .catch(err => {
            console.error('Error:', err);
            feedbackText.textContent = 'Error assessing your answer.';
            feedbackContainer.style.display = 'block';
        });
    });
});