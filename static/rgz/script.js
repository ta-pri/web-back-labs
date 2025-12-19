let currentPage = 1;

async function loadBooks() {
    const title = document.getElementById('f-title').value;
    const author = document.getElementById('f-author').value;
    const publisher = document.getElementById('f-publisher').value;
    const min = document.getElementById('f-min').value;
    const max = document.getElementById('f-max').value;
    const sort = document.getElementById('sort-by').value;

    const url = new URL('/rgz/api/books', window.location.origin);
    url.searchParams.append('page', currentPage);
    if (title) url.searchParams.append('title', title);
    if (author) url.searchParams.append('author', author);
    if (publisher) url.searchParams.append('publisher', publisher);
    if (min) url.searchParams.append('min_pages', min);
    if (max) url.searchParams.append('max_pages', max);
    url.searchParams.append('sort_by', sort);

    const response = await fetch(url);
    const data = await response.json();

    const container = document.getElementById('books-container');
    container.innerHTML = '';
    
    data.books.forEach(book => {
        const div = document.createElement('div');
        div.className = 'book-card';
        
        let imageSrc = book.cover_url;
        
        if (!imageSrc || imageSrc === "https://via.placeholder.com/150") {
            imageSrc = "/static/rgz/book_placeholder.jpg"; 
        }

        div.innerHTML = `
            <img src="${imageSrc}" alt="Обложка" onerror="this.src='/static/rgz/book_placeholder.jpg'">
            <div class="book-title">${book.title}</div>
            <div style="font-style:italic;">${book.author}</div>
            <div style="font-size:0.9em; color:#666; margin-top: auto;">
                ${book.pages} стр.<br>${book.publisher}
            </div>
        `;
        container.appendChild(div);
    });

    document.getElementById('results-info').innerText = `Всего найдено: ${data.total}`;
    document.getElementById('page-num').innerText = currentPage;
    
    document.getElementById('prev-btn').disabled = (currentPage === 1);
    document.getElementById('next-btn').disabled = (currentPage >= data.pages_total);
}
function changePage(dir) {
    currentPage += dir;
    loadBooks();
    window.scrollTo(0, 0);
}

function applyFilters() {
    currentPage = 1;
    loadBooks();
}

function resetFilters() {
    document.querySelectorAll('input').forEach(i => i.value = '');
    currentPage = 1;
    loadBooks();
}

document.addEventListener('DOMContentLoaded', loadBooks);