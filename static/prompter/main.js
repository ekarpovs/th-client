// @ts-nocheck
// Be interactions
const THCL_LOCATOR = 'https://th-zero.onrender.com';

// Get data from backend
async function fetchData(lang = 'ru') {
  const url = `${THCL_LOCATOR}/webdata/${lang}`;
  const response = await fetch(url);
  if (response.ok) {
      const result = await response.json();  
      // now do something with the result
      // console.log("RESULT", result);
      return result;
  } else {
      alert(response.status);
      return {};
  }
};

// Push data to backend
async function sendMessageIndex(index) {
  const url = `${THCL_LOCATOR}/redirect`;
  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify({
      message: index,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    } 
  });
  if (response.ok) {
      return {};
  } else {
      alert(response.status);
      return {};
  }
};
// @ts-nocheck
// Selectors
const smallSelectorBtn = document.querySelector('#small-font-size-selector');
const mediumSelectorBtn = document.querySelector('#medium-font-size-selector');
const largeSelectorBtn = document.querySelector('#large-font-size-selector');

const enSelectorBtn = document.querySelector('#en-language-selector');
const heSelectorBtn = document.querySelector('#he-language-selector');
const ruSelectorBtn = document.querySelector('#ru-language-selector');

const resetChatBtn = document.querySelector('#reset-chat-button');
const resetStartFrom = document.querySelector('#reset-start-from');

let currentFontSize = 'S';

const changeFontSize = (size) => {
  currentFontSize = size
  // Change the buttons color
  if (size === 'S') {
    smallSelectorBtn.classList.add('current-font-size');
    mediumSelectorBtn.classList.remove('current-font-size');
    largeSelectorBtn.classList.remove('current-font-size');
  }
  if (size === 'M') {
    mediumSelectorBtn.classList.add('current-font-size');
    smallSelectorBtn.classList.remove('current-font-size');
    largeSelectorBtn.classList.remove('current-font-size');
  }

  if (size === 'L') {
    largeSelectorBtn.classList.add('current-font-size');
    smallSelectorBtn.classList.remove('current-font-size');
    mediumSelectorBtn.classList.remove('current-font-size');
  }

  console.log(currentFontSize);

  if (currentFontSize != size) {
    currentFontSize = size;
    console.log(currentFontSize);
  }

  // /* auto-focus the input field */
  // chatInput.focus()
};

smallSelectorBtn.onclick = () => changeFontSize('S');
mediumSelectorBtn.onclick = () => changeFontSize('M');
largeSelectorBtn.onclick = () => changeFontSize('L');


// let currentLanguage = 'En';

// const changeLanguage = (lang) => {

//   if (lang === 'En') {
//     enSelectorBtn.classList.add('current-language');
//     heSelectorBtn.classList.remove('current-language');
//     ruSelectorBtn.classList.remove('current-language');
//   }
//   if (lang === 'He') {
//     heSelectorBtn.classList.add('current-language');
//     enSelectorBtn.classList.remove('current-language');
//     ruSelectorBtn.classList.remove('current-language');
//   }

//   if (lang === 'Ru') {
//     ruSelectorBtn.classList.add('current-language');
//     enSelectorBtn.classList.remove('current-language');
//     heSelectorBtn.classList.remove('current-language');
//   }

//   console.log(currentLanguage);

//   if (currentLanguage != lang) {
//     currentLanguage = lang;
//     console.log(currentLanguage);
//   }

// }
// @ts-nocheck
// Create regular message
const createChatMessageElement = (message, id) => `
    <div class="message multiline" id=${id}>
    <div class="message-text">${message}</div>
    </div>
`
// Add top margin for shift to the bottom
const doMessageFirst = (index) => {
	const mess = document.querySelector(`#message${index}`);
	mess.classList.add('first-message');
};

const doMessageCurrent = (currentMessageIndexShift) => {
	const chatMessages = document.querySelector('#chat-messages');
	const messagesLength = chatMessages.childElementCount;
	console.log("messagesLength", messagesLength);

	if ((messagesLength > currentMessageIndexShift)) {
		// Do the message font large and change background
		const curMess = chatMessages.children[messagesLength - (currentMessageIndexShift + 1)];
		curMess.classList.add('current-message');

		// Do the message font normal and restore background
		if (messagesLength > (currentMessageIndexShift + 1)) {
			const mess = chatMessages.children[messagesLength - (currentMessageIndexShift + 2)];
			mess.classList.remove('current-message');
		}
	}
};

// @ts-nocheck
document.addEventListener('DOMContentLoaded', () => {
  // Chat
  // Constants
  const chatHeader = document.querySelector('.chat-header');
  const chatMessages = document.querySelector('.chat-messages');
  const nextBtn = document.querySelector('.next-button');
  const messCounter = document.querySelector('.counter');
  const settingSpan = document.querySelector('.settings-span');
  const closeButton = document.getElementById('close');
  const smallSize = document.getElementById('small-font-size-selector');
  const mediumSize = document.getElementById('medium-font-size-selector');
  const largeSize = document.getElementById('large-font-size-selector');


  // Define number of messages from bottom
  const currentMessageIndexShift = 2;

  // Initialization
  chatHeader.innerHTML = '';
  let subTitles = [];
  let messageIndex = 0;

  fetchData().then( data => {
    const content = data.content;
    // The first line is the play Title
    const playTitle = data.content[0].chank;
    chatHeader.innerHTML = playTitle;
    subTitles = content.slice(1);
    // Show the first subset
    createInitialMessagesSubset();
  });

  const updateCounter = (index) => {
    messCounter.innerHTML = (index) + ' / ' + subTitles.length;
  };  

  const markMessage = (startFrom) => {
    if (messageIndex === startFrom) {
      doMessageFirst(messageIndex);
    }
    doMessageCurrent(currentMessageIndexShift);
  };

  const nextMessage = (e) => {
    e.preventDefault();

    const startFrom = Number(resetStartFrom.value);
    resetStartFrom.value = "";
    console.log("startFrom", startFrom);
    
    let index = messageIndex - currentMessageIndexShift - 1;
    if (messageIndex < subTitles.length) {
      createNewMessage(startFrom);
      messageIndex++;
      updateCounter(index + currentMessageIndexShift - 1);
    } 
    else if (messageIndex < subTitles.length + currentMessageIndexShift + 1) {
      messageIndex++;
      updateCounter(index + currentMessageIndexShift - 1);
    }
    else {
      index = -9999
    }
    
    sendMessageIndex(index).then( data => {
      console.log(index);
    })
  };

  const createInitialMessagesSubset = (startFrom = 0) => {
    for (let i = 0; i <= currentMessageIndexShift; i++) {
      createNewMessage(startFrom);
      messageIndex++;
    }
    updateCounter(0);
  };

  const createNewMessage = (startFrom) => {
    
    const message = subTitles[messageIndex];
    const messageText = message.chank;

    /* Add message to DOM */
    const newMessageElement = createChatMessageElement(messageText, 'message' + messageIndex);
    chatMessages.innerHTML += newMessageElement;
    markMessage(startFrom);

    /*  Scroll to bottom of chat messages */
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  // Set event handlers
  nextBtn.addEventListener('click', nextMessage);

  resetChatBtn.addEventListener('click', () => {
    const startFrom = Number(resetStartFrom.value);
    console.log("resetStartFrom", startFrom);

    // Clean clients
    chatMessages.innerHTML = '';
    messageIndex = startFrom;
    createInitialMessagesSubset(startFrom);
    sendMessageIndex(-10000).then( data => {
      console.log("sent", -10000);
    }); 
  });
  
  settingSpan.addEventListener('click', () => {
    const popup = document.getElementById('popup');
    popup.style.display = 'block';
  });

  closeButton.addEventListener('click', () => {
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
  });

  smallSize.addEventListener('click', () => {
    const chatMessages = document.getElementById('chat-messages')
    chatMessages.style.fontSize = "0.95em";
  });

  mediumSize.addEventListener('click', () => {
    const chatMessages = document.getElementById('chat-messages')
    chatMessages.style.fontSize = "1.25em";
  });

  largeSize.addEventListener('click', () => {
    const chatMessages = document.getElementById('chat-messages')
    chatMessages.style.fontSize = "1.45em";
  });
});
