const vscode = require('vscode');
const fetch = require('node-fetch');

async function askAssistant(prompt) {
    const endpoint = vscode.workspace.getConfiguration('aiAssistant').get('endpoint') || 'http://127.0.0.1:5000/chat';
    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const data = await res.json();
        return data.reply || 'No reply from assistant.';
    } catch (e) {
        return '[error contacting assistant: ' + String(e) + ']';
    }
}

function activate(context) {
    let disposable = vscode.commands.registerCommand('ai-assistant.ask', async function () {
        const q = await vscode.window.showInputBox({ prompt: 'Ask the AI assistant about selected code or the repo' });
        if (!q) return;
        vscode.window.showInformationMessage('Querying assistant...');
        const reply = await askAssistant(q);
        vscode.window.showInformationMessage('Assistant: ' + reply.substring(0, 200));
    });
    context.subscriptions.push(disposable);
}

function deactivate() {}
module.exports = { activate, deactivate };
