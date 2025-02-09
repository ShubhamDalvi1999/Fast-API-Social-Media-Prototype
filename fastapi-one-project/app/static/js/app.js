// DOM Elements
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const authForms = document.getElementById('authForms');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const postsSection = document.getElementById('postsSection');
const createPostForm = document.getElementById('createPostForm');
const postsList = document.getElementById('postsList');
const navButtons = document.getElementById('navButtons');

// State
let token = localStorage.getItem('token');
let currentUser = null;

// Show/Hide UI based on auth state
function updateUI() {
    if (token) {
        navButtons.innerHTML = `
            <span class="text-gray-500">Welcome, ${currentUser?.username || 'User'}</span>
            <a href="#" class="py-2 px-4 text-gray-500 hover:text-gray-700" onclick="logout()">Logout</a>
        `;
        authForms.classList.add('hidden');
        postsSection.classList.remove('hidden');
        loadPosts();
    } else {
        navButtons.innerHTML = `
            <a href="#" class="py-2 px-4 text-gray-500 hover:text-gray-700" id="loginBtn">Login</a>
            <a href="#" class="py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600" id="registerBtn">Register</a>
        `;
        authForms.classList.remove('hidden');
        postsSection.classList.add('hidden');
        attachAuthListeners();
    }
}

// Event Listeners
function attachAuthListeners() {
    document.getElementById('loginBtn')?.addEventListener('click', () => {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
    });

    document.getElementById('registerBtn')?.addEventListener('click', () => {
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
    });
}

// API Calls
async function login(username, password) {
    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch('/api/v1/auth/token', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }

        token = data.access_token;
        localStorage.setItem('token', token);
        await getCurrentUser();
        if (currentUser) {
            console.log('Login successful:', currentUser);
            // Clear any previous error messages
            const errorDiv = document.getElementById('login-error');
            if (errorDiv) {
                errorDiv.classList.add('hidden');
            }
            updateUI();
        } else {
            throw new Error('Failed to get user information after login');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('login-error', error.message);
    }
}

// Helper function to show errors
function showError(elementId, message) {
    const errorDiv = document.getElementById(elementId);
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    } else {
        alert(message);
    }
}

async function register(username, email, password) {
    try {
        const response = await fetch('/api/v1/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }

        console.log('Registration successful:', data);
        await login(username, password);
    } catch (error) {
        console.error('Registration error:', error);
        showError('register-error', error.message);
    }
}

async function getCurrentUser() {
    try {
        const response = await fetch('/api/v1/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to get user info');
        }

        currentUser = await response.json();
        console.log('Current user:', currentUser);
    } catch (error) {
        console.error('Error getting user info:', error);
        token = null;
        localStorage.removeItem('token');
        updateUI();
    }
}

async function createPost(content) {
    try {
        const response = await fetch('/api/v1/posts/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to create post');
        }

        showMessage('success-message', 'Post created successfully');
        await loadPosts();
    } catch (error) {
        console.error('Failed to create post:', error);
        showMessage('error-message', error.message);
    }
}

async function loadPosts() {
    try {
        const response = await fetch('/api/v1/posts/with_counts/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Failed to load posts');

        const posts = await response.json();
        displayPosts(posts);
    } catch (error) {
        console.error('Error loading posts:', error);
    }
}

function displayPosts(posts) {
    console.log('Displaying posts:', posts); // Debug log
    postsList.innerHTML = posts.map(post => `
        <div id="post-${post.id}" class="post animate-fade-in">
            <div class="post-header">
                <div>
                    <h3 class="font-bold">${post.owner_username}</h3>
                    <p class="post-meta">${new Date(post.timestamp).toLocaleString()}</p>
                </div>
                ${post.is_owner ? `
                    <div class="post-actions">
                        <button onclick="deletePost(${post.id})" class="btn btn-danger">
                            <span class="delete-icon">🗑️</span> Delete
                        </button>
                    </div>
                ` : ''}
            </div>
            <div class="post-content">
                <p>${post.content}</p>
            </div>
            <div class="post-footer">
                <button onclick="toggleLike(${post.id})" class="post-action">
                    ❤️ ${post.likes_count || 0}
                </button>
                <button onclick="toggleRetweet(${post.id})" class="post-action">
                    🔄 ${post.retweets_count || 0}
                </button>
            </div>
        </div>
    `).join('');
}

async function deletePost(postId) {
    try {
        if (!confirm('Are you sure you want to delete this post?')) {
            return;
        }

        const post = document.getElementById(`post-${postId}`);
        if (post) {
            post.classList.add('loading');
        }

        const response = await fetch(`/api/v1/posts/${postId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        const contentType = response.headers.get('content-type');
        let data;
        
        try {
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = { detail: await response.text() };
            }
        } catch (e) {
            console.error('Error parsing response:', e);
            data = { detail: 'Error processing server response' };
        }

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to delete post');
        }

        showMessage('success-message', data.message || 'Post deleted successfully');
        await loadPosts();
    } catch (error) {
        console.error('Delete error:', error);
        showMessage('error-message', error.message);
    } finally {
        const post = document.getElementById(`post-${postId}`);
        if (post) {
            post.classList.remove('loading');
        }
    }
}

// Helper function to show messages (success or error)
function showMessage(type, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type} animate-fade-in`;
    messageDiv.textContent = message;
    
    // Add to the top of the posts container
    const postsContainer = document.querySelector('.posts-container');
    if (postsContainer) {
        postsContainer.insertBefore(messageDiv, postsContainer.firstChild);
        
        // Remove the message after 3 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}

async function toggleLike(postId) {
    try {
        const response = await fetch(`/api/v1/posts/${postId}/like`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Failed to toggle like');

        await loadPosts();
    } catch (error) {
        console.error('Error toggling like:', error);
    }
}

async function toggleRetweet(postId) {
    try {
        const response = await fetch(`/api/v1/posts/${postId}/retweet`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Failed to toggle retweet');

        await loadPosts();
    } catch (error) {
        console.error('Error toggling retweet:', error);
    }
}

function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('token');
    updateUI();
}

// Form Submissions
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    // Clear previous error
    const errorDiv = document.getElementById('login-error');
    if (errorDiv) {
        errorDiv.classList.add('hidden');
    }
    
    if (!username || !password) {
        showError('login-error', 'Please enter both username and password');
        return;
    }
    
    await login(username, password);
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    // Clear previous error
    const errorDiv = document.getElementById('register-error');
    if (errorDiv) {
        errorDiv.classList.add('hidden');
    }
    
    if (!username || !email || !password) {
        showError('register-error', 'Please fill in all fields');
        return;
    }
    
    await register(username, email, password);
});

createPostForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const content = createPostForm.content.value;
    if (!content.trim()) {
        alert('Please enter some content for your post');
        return;
    }
    await createPost(content);
    createPostForm.content.value = '';
});

// Initialize UI
updateUI(); 

// Add a function to check if a post is owned by the current user
function isPostOwner(post) {
    return currentUser && post.owner_id === currentUser.id;
} 