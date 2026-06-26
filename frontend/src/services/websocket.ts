export class WebSocketClient {
  private ws: WebSocket | null = null

  connect(url: string, onMessage: (data: unknown) => void) {
    this.disconnect()
    this.ws = new WebSocket(url)
    this.ws.onmessage = (event) => {
      try {
        onMessage(JSON.parse(event.data))
      } catch {
        onMessage(event.data)
      }
    }
  }

  send(data: unknown) {
    this.ws?.send(JSON.stringify(data))
  }

  disconnect() {
    this.ws?.close()
    this.ws = null
  }
}