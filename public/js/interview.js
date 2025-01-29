document.addEventListener('DOMContentLoaded', () => {
    const speechBtn = document.getElementById('speech-btn');
    const questionContainer = document.getElementById('question-container');
    const questionElement = document.getElementById('question');
    const listenQuestionBtn = document.getElementById('listen-question-btn');
    const answerTextarea = document.getElementById('answer');
    const submitAnswerBtn = document.getElementById('submit-answer-btn');
    const feedbackElement = document.getElementById('feedback');

    let currentQuestion = '';
    const questions = [
        "Tell me about yourself.",
        "Why do you want to work for our company?",
        "Describe a challenging situation you faced and how you handled it."
    ];

    function getRandomQuestion() {
        const index = Math.floor(Math.random() * questions.length);
        return questions[index];
    }

    speechBtn.addEventListener('click', () => {
        currentQuestion = getRandomQuestion();
        questionElement.textContent = currentQuestion;
        questionContainer.style.display = 'block';
    });

    submitAnswerBtn.addEventListener('click', async () => {
        const answer = answerTextarea.value;
        try {
            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ answer }),
            });
            const data = await response.json();
            feedbackElement.textContent = data.feedback;
        } catch (error) {
            console.error('Error:', error);
            feedbackElement.textContent = 'Error getting feedback. Please try again.';
        }
    });

    if ('speechSynthesis' in window) {
        listenQuestionBtn.addEventListener('click', () => {
            const utterance = new SpeechSynthesisUtterance(currentQuestion);
            speechSynthesis.speak(utterance);
        });
    } else {
        listenQuestionBtn.style.display = 'none';
    }
});