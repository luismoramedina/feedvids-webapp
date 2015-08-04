//var applicationID = '794B7BBF';
var applicationID = '9867D8B4';
var namespace = 'urn:x-cast:com.google.cast.sample.helloworld';
var session = null;

if (!chrome.cast || !chrome.cast.isAvailable) {
    setTimeout(initializeCastApi, 1000);
}

function initializeCastApi() {
    var sessionRequest = new chrome.cast.SessionRequest(applicationID);
    var apiConfig = new chrome.cast.ApiConfig(sessionRequest,
        onSessionListener,
        onReceiverListener);

    chrome.cast.initialize(apiConfig, onInitSuccess, onError);
}

function onInitSuccess() {
    log("onInitSuccess");
}

function onSuccess(message) {
    log("onSuccess: " + message);
}

function onStopAppSuccess() {
    log('onStopAppSuccess');
}

function onSessionListener(e) {
    log('New session:' + e.sessionId);
    session = e;
    session.addUpdateListener(sessionUpdateListener);
    session.addMessageListener(namespace, onReceiverMessage);
}

function sessionUpdateListener(isAlive) {
    //TODO maybe request a new session
    log("session change, alive? " + isAlive);
    if (!isAlive) {
        log(session.sessionId + " removed");
        session = null;
        updateInterfaceOnSession();
    }
}

function updateInterfaceOnSession() {
    if (isCasting()) {
        $("#cast_button_image").attr("src","img/ic_media_route_on_holo_light.png");
    } else {
        $("#cast_button_image").attr("src","img/ic_media_route_off_holo_light.png");
    }
}

function onReceiverMessage(namespace, message) {
    log("message from receiver: " + ", " + message + "(" + namespace + ")");
}

function onReceiverListener(e) {
    if (e === 'available') {
        log("receiver found");
    }
    else {
        log("receiver list empty");
    }
}

function stopApp() {
    session.stop(onStopAppSuccess, onError);
}

function onRequestSessionSuccess(e) {
    log("request session ok: " + e.sessionId)
    session = e;
    session.addMessageListener(namespace, onReceiverMessage);
    session.addUpdateListener(sessionUpdateListener);
    updateInterfaceOnSession();
}

function onLaunchError(message) {
    log("onLaunchError: " + JSON.stringify(message));
}

function onError(message) {
    log("onError: " + JSON.stringify(message));
}

function sendToReceiver(message) {
    if (session == null) {
        chrome.cast.requestSession(onRequestSessionSuccess, onLaunchError);
    } else {
        session.sendMessage(namespace, message, onSuccess.bind(this, "Message sent: " + message), onError);
    }
}

function log(message) {
    console.log(message);
}

function isCasting() {
    return session != null;
}