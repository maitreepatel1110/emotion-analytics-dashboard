fetch('/data')
  .then(response => response.json())
  .then(data => {
    const timestamps = data.map(row => row.Timestamp);
    const emotions = data.map(row => row.Emotion);

    // Group data by emotion
    const emotionCounts = {};
    const emotionTimeline = {};

    for (let i = 0; i < emotions.length; i++) {
        const emotion = emotions[i];
        const time = timestamps[i];

        emotionCounts[emotion] = (emotionCounts[emotion] || 0) + 1;

        if (!emotionTimeline[emotion]) {
            emotionTimeline[emotion] = [];
        }
        emotionTimeline[emotion].push({ x: time, y: emotionTimeline[emotion].length + 1 });
    }

    const colors = {
        Neutral: '#9ad0ec',
        Happy: '#f4a261',
        Sad: '#a29bfe',
        Angry: '#ef476f',
        Fear: '#a8dadc',
        Surprise: '#d4a373',
        Disgust: '#8d99ae'
    };

    // Line chart: Emotion trends over time
    new Chart(document.getElementById('trendChart'), {
        type: 'line',
        data: {
            datasets: Object.keys(emotionTimeline).map(emotion => ({
                label: emotion,
                data: emotionTimeline[emotion],
                borderColor: colors[emotion] || '#000',
                backgroundColor: 'transparent',
                fill: false,
                tension: 0.4
            }))
        },
        options: {
            scales: {
                x: { type: 'time', time: { unit: 'minute' }, title: { display: true, text: 'Time' }},
                y: { beginAtZero: true, title: { display: true, text: 'Occurrences' }}
            }
        }
    });

    // Bar chart: Total count per emotion
    const labels = Object.keys(emotionCounts);
    const counts = Object.values(emotionCounts);
    const peakEmotion = labels[counts.indexOf(Math.max(...counts))];

    document.getElementById('peakEmotionLabel').innerText = peakEmotion;

    new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Count',
                data: counts,
                backgroundColor: labels.map(e => colors[e] || '#888')
            }]
        },
        options: {
            indexAxis: 'x',
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Pie chart: Proportion of each emotion
    new Chart(document.getElementById('pieChart'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Emotion Share',
                data: counts,
                backgroundColor: labels.map(e => colors[e] || '#ccc')
            }]
        }
    });
  });
