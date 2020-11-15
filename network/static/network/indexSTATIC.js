document.addEventListener('DOMContentLoaded', () => {



})


function verify() {
    let textarea = document.querySelector('#textarea-to-post')
    if(textarea.value.length > 0) {
        document.querySelector('#submit-to-post').disabled = false
    } else {
        document.querySelector('#submit-to-post').disabled = true
    }
}

function likeButton(button) {
    if(button.className === 'like-button-open'){
        button.innerHTML = 'Liked'
        button.value = 'close'
        button.className = 'like-button-close'
        let number_of_likes = document.querySelector(`#likes-${button.id}`)
        likes = parseInt(number_of_likes.textContent) + 1
        number_of_likes.innerHTML = likes
        like(button)
    } else if (button.className === 'like-button-close'){
        button.innerHTML = 'Like'
        button.value = 'open'
        button.className = 'like-button-open'
        let number_of_likes = document.querySelector(`#likes-${button.id}`)
        likes = parseInt(number_of_likes.textContent) - 1
        number_of_likes.innerHTML = likes
        dislike(button)
    }
}

function like(button) {
    
    fetch('/makeLike', {
        method: 'PUT',
        body: JSON.stringify({
            post_id: button.id,
            is_like: true
        })
      })

}

function dislike(button) {

    fetch('/makeLike', {
        method: 'PUT',
        body: JSON.stringify({
            post_id: button.id,
            is_like: false
        })
      })
}

function editPost(div_edit) {

    post_id = div_edit.dataset.post
    textarea = document.querySelector(`#textarea-${post_id}`)
    textarea.disabled = false

    div_finish_edit = document.querySelector(`#finish-edit-${post_id}`)
    div_finish_edit.style.display = 'block'
    div_edit.style.display = 'none'

}

function finishEditPost(div_finish_edit) {

    post_id = div_finish_edit.dataset.post
    textarea = document.querySelector(`#textarea-${post_id}`)
    content = textarea.value

    if(verifyText(content)) {
        return alert('posts can not be blank')
    }

    textarea.disabled = true
    textarea.value = content
    div_edit = document.querySelector(`#edit-${post_id}`)
    div_finish_edit.style.display = 'none'
    div_edit.style.display = 'block'
    
    doFetch(post_id, content)
}

function doFetch(post_id, content) {

    fetch(`/edit/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content:content
        })
    })
}

function verifyText(content) {

    if(content.length === 0) {
        return true
    } return false
}

