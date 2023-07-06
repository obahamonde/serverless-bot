from string import Template

from pydantic import BaseModel, Field


class WidgetModel(BaseModel):
    api_url: str = Field(...)
    namespace: str = Field(...)
    bot_name:str = Field(default="AI assistant")
    text_color: str = Field(default="#008080")
    bg_color: str = Field(default="#eeeeee")
    error_color: str = Field(default="#fcc000")
    error_bg_color: str = Field(default="#ea0000")

def Widget(model: WidgetModel):
    """Creates the embeddable widget for the Chatbot."""
    text = """
    <header></header>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,1,0');

* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
body {
  background-color: $bg_color;
  font-family: 'Poppins', sans-serif;
}
.chatbot__button {
  position: fixed;
  bottom: 35px;
  right: 40px;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: $bg_color;
  color: $text_color;
  border: none;
  border-radius: 50%;
  outline: none;
  cursor: pointer;
}
.chatbot__button span {
  position: absolute;
}
.show-chatbot .chatbot__button span:first-child,
.chatbot__button span:last-child {
  opacity: 0;
}
.show-chatbot .chatbot__button span:last-child {
  opacity: 1;
}
.chatbot {
  position: fixed;
  bottom: 100px;
  right: 40px;
  width: 420px;
  background-color: $bg_color;
  border-radius: 15px;
  box-shadow: 0 0 128px 0 rgba(0, 0, 0, 0.1) 0 32px 64px -48px rgba(0, 0, 0, 0.5);
  transform: scale(0.5);
  transition: transform 0.3s ease;
  overflow: hidden;
  opacity: 0;
  pointer-events: none;
}
.show-chatbot .chatbot {
  opacity: 1;
  pointer-events: auto;
  transform: scale(1);
}
.chatbot__header {
  position: relative;
  background-color: $bg_color;
  text-align: center;
  padding: 16px 0;
}
.chatbot__header span {
  display: none;
  position: absolute;
  top: 50%;
  right: 20px;
  color: $text_color;
  transform: translateY(-50%);
  cursor: pointer;
}
.chatbox__title {
  font-size: 1.4rem;
  color: $text_color;
}
.chatbot__box {
  height: 510px;
  overflow-y: auto;
  padding: 30px 20px 100px;
}
.chatbot__chat {
  display: flex;
}
.chatbot__chat p {
  max-width: 75%;
  font-size: 0.95rem;
  white-space: pre-wrap;
  color: $text_color;
  background-color: $bg_color;
  border-radius: 10px 10px 0 10px;
  padding: 12px 16px;
}
.chatbot__chat p.error {
  color: $error_color;
  background: $error_bg_color;
}
.incoming p {
  color: $text_color;
  background: $bg_color;
  border-radius: 10px 10px 10px 0;
}
.incoming span {
  width: 32px;
  height: 32px;
  line-height: 32px;
  color: $text_color;
  background-color: $bg_color;
  border-radius: 4px;
  text-align: center;
  align-self: flex-end;
  margin: 0 10px 7px 0;
}
.outgoing {
  justify-content: flex-end;
  margin: 20px 0;
}
.incoming {
  margin: 20px 0;
}
.chatbot__input-box {
  position: absolute;
  bottom: 0;
  width: 100%;
  display: flex;
  gap: 5px;
  align-items: center;
  border-top: 1px solid $text_color;
  background: #f3f7f8;
  padding: 5px 20px;
}
.chatbot__textarea {
  width: 100%;
  min-height: 55px;
  max-height: 180px;
  font-size: 0.95rem;
  padding: 16px 15px 16px 0;
  color: $text_color;
  border: none;
  outline: none;
  resize: none;
  background: transparent;
}
.chatbot__textarea::placeholder {
  font-family: 'Poppins', sans-serif;
}
.chatbot__input-box span {
  font-size: 1.75rem;
  color: $text_color;
  cursor: pointer;
  visibility: hidden;
}
.chatbot__textarea:valid ~ span {
  visibility: visible;
}

@media (max-width: 490px) {
  .chatbot {
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    border-radius: 0;
  }
  .chatbot__box {
    height: 90%;
  }
  .chatbot__header span {
    display: inline;
  }
}   
</style>
<button class="chatbot__button">
    <span class="material-symbols-outlined">mode_comment</span>
    <span class="material-symbols-outlined">close</span>
  </button>
  <div class="chatbot">
    <div class="chatbot__header">
      <h3 class="chatbox__title">$bot_name</h3>
      <span class="material-symbols-outlined">close</span>
    </div>
    <ul class="chatbot__box">
      <li class="chatbot__chat incoming">
        <span class="material-symbols-outlined">smart_toy</span>
        <p>Hi there. How can I help you today?</p>
      </li>
      <li class="chatbot__chat outgoing">
        <p>...</p>
      </li>
    </ul>
    <div class="chatbot__input-box">
      <textarea
        class="chatbot__textarea"
        placeholder="Enter a message..."
        required
      ></textarea>
      <span id="send-btn" class="material-symbols-outlined">send</span>
    </div>
  </div>
<script>
    const sel = (selector) => document.querySelector(selector);
const chatbotToggle = sel('.chatbot__button');
const sendChatBtn = sel('.chatbot__input-box span');
const chatInput = sel('.chatbot__textarea');
const chatBox = sel('.chatbot__box');
const chatbotCloseBtn = sel('.chatbot__header span');

let userMessage;
// Need GPT key
const inputInitHeight = chatInput.scrollHeight;


const createChatLi = (message, className) => {
  const chatLi = document.createElement('li');
  chatLi.classList.add('chatbot__chat', className);
  let chatContent =
    className === 'outgoing'
      ? `<p></p>`
      : `<span class="material-symbols-outlined">smart_toy</span> <p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector('p').textContent = message;
  return chatLi;
};

const generateResponse = (incomingChatLi) => {
  const API_URL = "$api_url";
  const messageElement = incomingChatLi.querySelector('p');

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      input: userMessage,
      namespace: "$namespace",
    }),
  };
  fetch(API_URL, requestOptions)
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      messageElement.textContent = data.response;
    })
    .catch((error) => {
      messageElement.classList.add('error');
      messageElement.textContent = 'Oops! Please try again!';
      console.log(error);
    })
    .finally(() => chatBox.scrollTo(0, chatBox.scrollHeight));
};

const handleChat = () => {
  userMessage = chatInput.value.trim();
  if (!userMessage) return;
  chatInput.value = '';
  chatInput.style.height = inputInitHeight + 'px';

  chatBox.appendChild(createChatLi(userMessage, 'outgoing'));
  chatBox.scrollTo(0, chatBox.scrollHeight);

  setTimeout(() => {
    const incomingChatLi = createChatLi('Thinking...', 'incoming');
    chatBox.appendChild(incomingChatLi);
    chatBox.scrollTo(0, chatBox.scrollHeight);
    generateResponse(incomingChatLi);
  }, 150);
};

chatInput.addEventListener('input', () => {
  chatInput.style.height = inputInitHeight + 'px';
  chatInput.style.height = chatInput.scrollHeight + 'px';
});
chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});
chatbotToggle.addEventListener('click', () =>
  document.body.classList.toggle('show-chatbot')
);
chatbotCloseBtn.addEventListener('click', () =>
  document.body.classList.remove('show-chatbot')
);
sendChatBtn.addEventListener('click', handleChat);
</script>
"""
    return Template(text).substitute(
        **model.dict())