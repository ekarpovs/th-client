// @ts-nocheck
// Be interactions
const THCL_LOCATOR = 'http://127.0.0.1:8021';

// const BSRV_LOCATOR = 'BROADCAST_SERVICE_URL';
// const ROOT_PATH = '/ws/socket.io';
// const TRANSPORTS = ['websocket', 'polling'];
// const RECONNECTION_ATTEMPTS =  5
// const ROOM = '2974528d-155d-42ed-aa01-37767a199fff';
// const CLIENT =  Date.now().toString(36) + Math.random().toString(36).substring(2);

// Initialize WebSocket connection with the authData
async function initializeSocket() {
  const cfg = await getConfig();
  console.log(cfg);  // Ensure cfg is fetched correctly

  // Assign the socket object to the global variable
  const sio = io(`${cfg.bsrvLocator}${cfg.authData['owner-type']}`, { 
      path: `${cfg.pathRoot}${cfg.authData['owner-type']}`,
      reconnectionAttempts: cfg.reconnectionAttempts,
      auth: cfg.authData,
      transports: cfg.transports,
  });

  // Handle connection
  sio.on('connect', () => {
    const mess = 'Connected to the server';
    console.log(mess);
    sendClientStatus('connected')
    setClientId(cfg.authData.client);
    sio.emit('join_room', cfg.authData.owner);
  });

  // socket.on('connected', function(data) {
  //   const status = `'connected' ${data}`
  //   console.log(status)
  //   clientStatus(status)
  //   setClientId(status)
  // });

  // Handle successful room join
  sio.on('room_joined', (room) => {
    const mess = `Joined room: ${room}`;
    console.log(mess);
  });

  // Handle room left
  sio.on('room_left', (room) => {
    const mess = `Left room: ${room}`;
    console.log(mess);
    sio.disconnect();
  });

  // socket.on('connect_error', function(data) {
  //   const status = `'connect_error' ${data}`
  //   console.log(status)
  //   sendClientStatus(status)
  //   setClientId(status)
  // });

  // Handle connection error
  sio.on('connect_error', (error) => {
    const mess = `connect error '${error}'`;
    console.error(mess);
    sendClientStatus(mess)
    setClientId(mess)
  });

  return sio;
}

// Get auth data
async function getConfig() {
  const url = `${THCL_LOCATOR}/cfg`;
  const response = await fetch(url);
  if (response.ok) {
      const result = await response.json();  
      return result;
  } else {
      const message = `error: ${response.status}, can't get config data`
      alert(message);
      return {};
  }
};

// Get data from backend
async function fetchData(lang = 'ru') {
  const url = `${THCL_LOCATOR}/webdata/${lang}`;
  const response = await fetch(url);
  if (response.ok) {
      const result = await response.json();  
      return result;
  } else {
      const message = `error: ${response.status}, can't get data`
      alert(message);
      return {};
  }
};

// Send connection info to backend
async function sendClientStatus(data='disconnected') {
  const url = `${THCL_LOCATOR}/status/${data}`;
  const response = await fetch(url);
  if (response.ok) {
      const result = await response.json();  
      console.log("status", result['status']);
      return result;
  } else {
      const message = `error: ${response.status}, can't get status`
      alert(message);
      return {};
  }
};
// @ts-nocheck
// Selectors
const clienIdHeader = document.getElementById('client-id')

const smallSelectorBtn = document.querySelector('#small-font-size-selector');
const mediumSelectorBtn = document.querySelector('#medium-font-size-selector');
const largeSelectorBtn = document.querySelector('#large-font-size-selector');

const enSelectorBtn = document.querySelector('#en-language-selector');
const heSelectorBtn = document.querySelector('#he-language-selector');
const ruSelectorBtn = document.querySelector('#ru-language-selector');

const setClientId = (id='disconnected') => {
  clienIdHeader.innerHTML = id;
};

let currentFontSize = 'M';

const changeFontSize = (size) => {
  currentFontSize = size;

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


let currentLanguage = 'Ru';

const changeLanguage = (lang) => {
  document.documentElement.dir = (lang === 'He') ? 'rtl' : 'ltr';
  currentLanguage = lang;

  if (lang === 'En') {
    enSelectorBtn.classList.add('current-language');
    heSelectorBtn.classList.remove('current-language');
    ruSelectorBtn.classList.remove('current-language');
  }
  if (lang === 'He') {
    heSelectorBtn.classList.add('current-language');
    enSelectorBtn.classList.remove('current-language');
    ruSelectorBtn.classList.remove('current-language');
  }

  if (lang === 'Ru') {
    ruSelectorBtn.classList.add('current-language');
    enSelectorBtn.classList.remove('current-language');
    heSelectorBtn.classList.remove('current-language');
  }

  if (currentLanguage != lang) {
    currentLanguage = lang;
    console.log(currentLanguage);
  }
};

enSelectorBtn.onclick = () => changeLanguage('En');
heSelectorBtn.onclick = () => changeLanguage('He');
ruSelectorBtn.onclick = () => changeLanguage('Ru');
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
	if (mess) {
		mess.classList.add('first-message');
	}
};
// Do font large and change background
const markMessageAsCurrernt = (index) => {
	const mess = document.querySelector(`#message${index}`);
	if (mess) {
		mess.classList.add('current-message');
	}
};
// Do font normal and restore background
const markMessageAsRegular = (index) => {
	const mess = document.querySelector(`#message${index}`);
	if (mess) {
		mess.classList.remove('current-message');
	}
};
// @ts-nocheck
document.addEventListener('DOMContentLoaded', () => {
  // Chat
  // Constants
  const chatHeader = document.querySelector('.chat-header');
  const chatMessages = document.querySelector('.chat-messages');
  const messCounter = document.querySelector('.counter');
  const settingSpan = document.querySelector('.settings-span');
  const closeButton = document.getElementById('close');
  const smallSize = document.getElementById('small-font-size-selector');
  const mediumSize = document.getElementById('medium-font-size-selector');
  const largeSize = document.getElementById('large-font-size-selector');
  const engLang = document.getElementById('en-language-selector');
  const hebLang = document.getElementById('he-language-selector');
  const rusLang = document.getElementById('ru-language-selector');

  // Initialization
  chatHeader.innerHTML = '';
  let subTitles = [];
  let messageIndex = 0;
  let resetFlag = false;

  // Call the function to initialize the WebSocket connection
  initializeSocket().then(socket => {
    socket.on('server-message', function(data) { 
      const index = Number(data);
      if (index === -9999) return;
      if (index === -10000) {
        resetMessanger();
      } else {
        createNewMessage(index);
      }
    });
  });

  setClientId();

  const updateCounter = (index) => {
    messCounter.innerHTML = (index + 1)  + ' / ' + subTitles.length;
  };

  fetchData().then( data => {
    const content = data.content;
    // The first line is the play Title
    const playTitle = data.content[0].chank;
    chatHeader.innerHTML = playTitle;
    subTitles = content.slice(1);
    updateCounter(-1);
  });
 
  const createNewMessage = (index) => {
    messageIndex = index;   
    const message = subTitles[messageIndex];
    messageText = message.chank;

    /* Add message to DOM */
    const newMessageElement = createChatMessageElement(messageText, 'message' + messageIndex);
    chatMessages.innerHTML += newMessageElement;
    updateCounter(messageIndex);

    if ((messageIndex === 0) || (resetFlag)) {
      doMessageFirst(messageIndex);
      resetFlag = false;
    }
     if ((messageIndex >= 0)) {   
      markMessageAsCurrernt(messageIndex); 
      if (messageIndex > 0) {
        markMessageAsRegular(messageIndex - 1);
      }
    }

    /*  Scroll to bottom of chat messages */
    chatMessages.scrollTop = chatMessages.scrollHeight
  };

  const resetMessanger =  () => {
    chatMessages.innerHTML = ''
    messageIndex = 0;
    updateCounter(-1);
    resetFlag = true;
  };

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

  engLang.addEventListener('click', () => {
    fetchData('en').then( data => {
      const content = data.content;
      // The first line is the play Title
      const playTitle = data.content[0].chank;
      chatHeader.innerHTML = playTitle;
      subTitles = content.slice(1);
      updateCounter(-1);
    });
  });

  hebLang.addEventListener('click', () => {
    fetchData('he').then( data => {
      const content = data.content;
      // The first line is the play Title
      const playTitle = data.content[0].chank;
      chatHeader.innerHTML = playTitle;
      subTitles = content.slice(1);
      updateCounter(-1);
    });
  });

  rusLang.addEventListener('click', () => {
    fetchData().then( data => {
      const content = data.content;
      // The first line is the play Title
      const playTitle = data.content[0].chank;
      chatHeader.innerHTML = playTitle;
      subTitles = content.slice(1);
      updateCounter(-1);
    });
  });
});
