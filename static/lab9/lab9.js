document.addEventListener('DOMContentLoaded', function() {
    const giftField = document.getElementById('gift-field');
    const openedCount = document.getElementById('opened-count');
    const remainingCount = document.getElementById('remaining-count');
    const message = document.getElementById('message');
    const result = document.getElementById('result');
    const giftImage = document.getElementById('gift-image');
    const congratulation = document.getElementById('congratulation');
    
    loadState();
    
    function loadState() {
        fetch('/lab9/state')
            .then(response => response.json())
            .then(data => {
                updateCounters(data.opened_count, data.remaining_count);
                renderBoxes(data.gifts);
            })
            .catch(error => {
                console.error('Ошибка загрузки состояния:', error);
                showMessage('Ошибка загрузки состояния', 'error');
            });
    }

    function renderBoxes(gifts) {
        giftField.innerHTML = '';
        gifts.forEach(gift => {
            const img = document.createElement('img');
            img.src = `/static/lab9/${gift.box_img}`;
            img.className = 'gift-box' + (gift.is_empty ? ' opened' : '');
            img.style.left = gift.left + '%';
            img.style.top = gift.top + '%';
            img.dataset.boxId = gift.id;
            
            if (!gift.is_empty) {
                img.style.cursor = 'pointer';
                img.onclick = () => openBox(gift.id);
            }
            giftField.appendChild(img);
        });
    }
    
    function openBox(boxId) {
        fetch('/lab9/open_box', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ box_id: boxId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCounters(data.opened_count, data.remaining_count);
                showGift(data.gift_image, data.congratulation);
                showMessage(data.message, 'success');
                loadState(); 
            } else {
                showMessage(data.message, 'error');
            }
        });
    }
    
    function updateCounters(opened, remaining) {
        openedCount.textContent = opened;
        remainingCount.textContent = remaining;
    }
    
    function showGift(giftImageUrl, congratulationText) {
        giftImage.src = giftImageUrl;
        congratulation.textContent = congratulationText;
        result.style.display = 'block';
    }
    
    function showMessage(text, type) {
        message.textContent = text;
        message.className = 'message ' + type;
        setTimeout(() => { message.textContent = ''; message.className = 'message'; }, 3000);
    }
});