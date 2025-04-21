const { app, BrowserWindow } = require('electron/main')

const createWindow = () => {
	const win = new BrowserWindow({
		width: 600,
		height: 500,
		resizable: true,
		//frame: false,
		//transparent: true
	})

	win.loadFile('index.html')
}

const nativeImage = require('electron').nativeImage;
const image = nativeImage.createFromPath('./paradocx-icon.png')
app.dock.setIcon(image);

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
