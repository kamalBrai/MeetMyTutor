document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded');
    const chatData = {{ chat_data| safe
}} || {
    "tutor1": {
        name: "Mr. Raj Sharma",
        avatar: "https://randomuser.me/api/portraits/men/12.jpg",
        isOnline: true,
        messages: [
            { id: 1, text: "Hi Mr. Sharma, I'm interested in your Physics tutoring for Grade 11.", sender: "student", time: "2025-07-13 10:30 AM" },
            { id: 2, text: "Hello! Yes, I received your request. I am available today.", sender: "tutor", time: "2025-07-13 10:35 AM" },
            { id: 3, text: "Tuesday evening sounds great! How about 6:00 PM?", sender: "student", time: "2025-07-13 10:40 AM" }
        ]
    },
    "tutor2": {
        name: "Admin Support",
        avatar: null,
        isOnline: false,
        messages: [
            { id: 4, text: "Your account is active and verified.", sender: "tutor", time: "2025-07-13 09:00 AM" },
            { id: 5, text: "Thank you for the update!", sender: "student", time: "2025-07-13 09:05 AM" }
        ]
    },
    "tutor3": {
        name: "Ms. Rita Sharma",
        avatar: "https://randomuser.me/api/portraits/women/45.jpg",
        isOnline: true,
        messages: [
            { id: 6, text: "I look forward to our session tomorrow.", sender: "tutor", time: "2025-07-13 05:00 PM" },
            { id: 7, text: "Me too!", sender: "student", time: "2025-07-13 05:05 PM" }
        ]
    }
};
console.log('chatData:', chatData);

const messageContainer = document.getElementById('messageContainer');
const chatListElement = document.getElementById('chatList');
const chatPartnerName = document.getElementById('chatPartnerName');
const chatHeaderAvatar = document.getElementById('chatHeaderAvatar');
const messagesDisplay = document.getElementById('messagesDisplay');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const headerOnlineIndicator = document.getElementById('headerOnlineIndicator');
const backToListBtn = document.getElementById('backToListBtn');
const welcomeMessage = document.getElementById('welcomeMessage');

console.log('messageContainer:', messageContainer);

let currentChatId = null;
let messageIdCounter = 8;

function getFormattedTime() {
    const now = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: 'numeric', minute: '2-digit', hour12: true };
    return now.toLocaleString('en-US', options);
}

function renderMessages() {
    welcomeMessage.classList.add('hidden');
    messagesDisplay.innerHTML = '';
    if (currentChatId === null) {
        welcomeMessage.classList.remove('hidden');
        return;
    }
    const chat = chatData[currentChatId];
    chatPartnerName.textContent = chat.name;
    if (chat.avatar) {
        chatHeaderAvatar.innerHTML = <img src="${chat.avatar}" alt="${chat.name}" class="w-full h-full object-cover">;
            } else {
                chatHeaderAvatar.innerHTML = <i class="bi bi-person-fill"></i>;
            }
            headerOnlineIndicator.style.display = chat.isOnline ? 'block' : 'none';
            if (chat.messages.length > 0) {
                chat.messages.forEach(msg => {
                    const isSent = msg.sender === 'student';
                    const bubble = document.createElement('div');
                    bubble.classList.add('max-w-[70%]', 'p-3', 'rounded-2xl', 'mb-4', 'break-words', isSent ? 'bg-blue-600' : 'bg-white', isSent ? 'text-white' : 'text-gray-800', isSent ? 'self-end' : 'self-start', isSent ? 'ml-auto' : 'mr-auto');
                    bubble.textContent = msg.text;
                    const timestamp = document.createElement('small');
                    timestamp.classList.add('text-xs', 'text-gray-500', 'block', 'mt-1', isSent ? 'text-right' : 'text-left');
                    timestamp.textContent = msg.time;
                    messagesDisplay.appendChild(bubble);
                    messagesDisplay.appendChild(timestamp);
                });
            messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
            } else {
                messagesDisplay.innerHTML = '<p class="text-center text-gray-500 mt-10">No messages yet. Start a conversation!</p>';
            }
        }

            function sendMessage() {
            const messageText = messageInput.value.trim();
            if (messageText === '' || currentChatId === null) return;
            const newMessage = {
                id: messageIdCounter++,
            text: messageText,
            sender: "student",
            time: getFormattedTime()
            };
            chatData[currentChatId].messages.push(newMessage);
            messageInput.value = '';
            renderMessages();
            setTimeout(() => simulateTutorReply(), 1000);
        }

            function simulateTutorReply() {
            if (currentChatId === null) return;
            const reply = "Got your message. I'll get back to you shortly!";
            const tutorMessage = {
                id: messageIdCounter++,
            text: reply,
            sender: "tutor",
            time: getFormattedTime()
            };
            chatData[currentChatId].messages.push(tutorMessage);
            renderMessages();
        }

            function showChatWindow() {
                messageContainer.classList.add('chat-selected');
            if (window.innerWidth < 768) {
                messageContainer.classList.add('show-chat');
            }
        }

            function showConversationsList() {
                messageContainer.classList.remove('show-chat');
            messageContainer.classList.remove('chat-selected');
            chatListElement.querySelectorAll('a').forEach(item => {
                item.classList.remove('active');
            });
            welcomeMessage.classList.remove('hidden');
            messagesDisplay.innerHTML = '';
        }

        chatListElement.addEventListener('click', (e) => {
            const listItem = e.target.closest('a');
            if (listItem) {
                chatListElement.querySelectorAll('a').forEach(item => {
                    item.classList.remove('active');
                });
            listItem.classList.add('active');
            currentChatId = listItem.dataset.chatId;
            renderMessages();
            showChatWindow();
            }
        });

            backToListBtn.addEventListener('click', showConversationsList);
            sendMessageBtn.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    });