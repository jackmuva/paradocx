const { app, BrowserWindow } = require('electron/main')

const createWindow = () => {
	const win = new BrowserWindow({
		width: 500,
		height: 300,
		resizable: true,
		//frame: false,
		//transparent: true
	})

	win.loadFile('index.html')
}

app.whenReady().then(() => {
	createWindow()

	app.on('activate', () => {
		if (BrowserWindow.getAllWindows().length === 0) {
			createWindow()
		}
	})
})

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit()
	}
})
