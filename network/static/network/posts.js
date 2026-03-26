document.addEventListener('DOMContentLoaded', () => {
    //Select all the edit buttons
    const edit_btns = document.querySelectorAll('.edit-btn');
    // If edit buttons exist:
    if (edit_btns.length > 0) {
        // Place event listeners to edit the post
        edit_btns.forEach((currentValue, currentIndex, listObj) => {
            currentValue.addEventListener('click', edit_post);
        });
    }
        
    
    // Select all the like buttons
    const like_btns = document.querySelectorAll('.like-btn');
    // If post buttons exist:
    if (like_btns.length > 0) {
        // Use ForEach!!
        // Place event listeners to like the post
        like_btns.forEach((currentValue, currentIndex, listObj) => {
            currentValue.addEventListener('click', like_post);
        })
    }
})


function edit_post(event) {
    const edit_btn = event.currentTarget;
    const post_paragraph= edit_btn.parentElement.querySelector('p');
    // Replace text paragrage with a textarea
    const post_textarea = document.createElement('textarea');
    post_textarea.value = post_paragraph.textContent;
    post_textarea.rows = 5;
    post_textarea.style.display = 'block';
    post_textarea.style.width = '100%';
    post_textarea.style.marginTop = '5px';
    post_textarea.style.marginBottom = '5px';
    post_paragraph.replaceWith(post_textarea); 
    // Create Save button and add the Save event listener 
    const save_btn = document.createElement('button');
    save_btn.classList = 'btn btn-secondary btn-sm save-btn';
    save_btn.dataset.post = `${edit_btn.dataset.post}`;
    save_btn.textContent = 'Save';
    save_btn.style.marginBottom = '5px';
    edit_btn.parentElement.appendChild(save_btn);
    save_btn.addEventListener('click', save_post);
    edit_btn.blur();
}

function save_post(event) {
    const save_btn = event.currentTarget;
    const post_textarea = save_btn.parentElement.querySelector('textarea');
    // Make the fetch call to edit the post
    fetch(`/posts/${save_btn.dataset.post}`, {
        method: 'PUT',
        body: JSON.stringify({"post-text": post_textarea.value})
    })
    // Promise Handler
    .then(response => response.json())
    .then(data => {
        if (data.error !== undefined) {
            throw new Error(`${error}`);
        }
        // Revert the textarea back to a text paragraph 
        const post_paragraph = document.createElement('p');
        post_paragraph.textContent = post_textarea.value;
        post_textarea.replaceWith(post_paragraph); 
        // Remove save button from the DOM
        save_btn.remove();
    })
    // Promise Catcher
    .catch(error => {
        alert(`${error}`);
    })
}


function like_post(event) {
    // Make the fetch call to like the post
    const btn = event.currentTarget;
    fetch(`/posts/${btn.dataset.post}`, {
        method: 'PUT',
        body: (btn.dataset.like === "y") ? JSON.stringify({"like": false}) : JSON.stringify({"like": true})
    })
    // Promise Handler
    .then(response => response.json())
    .then(data => {
        if (data.error !== undefined) {
            throw new Error(`${data.error}`);
        }
        // Successful request
        // Update button state (data-like & active state)
        if (btn.dataset.like === "y") {
            btn.dataset.like = "n";
            btn.classList.remove("active");
        }
        else {
            btn.dataset.like = "y";
            btn.classList.add("active");
        }
        // Update like count
        const likes = btn.parentElement.querySelector('.likes');
        likes.textContent = `${data.likes}`;
        btn.blur()
    })
    // Promise Catcher
    .catch(error => {
        alert(`${error}`);
    });
}