function followButton(button) {

    user_page = button.dataset.id

    if(button.className === 'link-follow') {
        button.className = 'link-following'
        button.innerHTML = 'Stop following'
        following = document.querySelector('#followers')
        number_followings = parseInt(following.textContent) + 1
        following.innerHTML = number_followings
        follow(user_page)
    } else {
        button.className = 'link-follow'
        button.innerHTML = 'Follow'
        following = document.querySelector('#followers')
        number_followings = parseInt(following.textContent) - 1
        following.innerHTML = number_followings
        unfollow(user_page)
    }

}

function follow(user_page) {
    
    fetch(`/follow/${user_page}`, {
        method: 'PUT',
        body: JSON.stringify({
            mode: 'follow'
        })
    })
}

function unfollow(user_page) {

    fetch(`/follow/${user_page}`, {
        method: 'PUT',
        body: JSON.stringify({
            mode: 'unfollow'
        })
    })
}

