let session = null;

chrome.tabs.onActivated.addListener(activeInfo => {
  chrome.tabs.get(activeInfo.tabId, tab => {
    if (!session || session.site !== tab.url) {
      if (session) {
        session.end = new Date().toISOString();
        chrome.storage.local.get({usage: []}, res => {
          const usage = res.usage;
          usage.push(session);
          chrome.storage.local.set({usage});
        });
      }
      session = {site: tab.url, start: new Date().toISOString()};
    }
  });
});
