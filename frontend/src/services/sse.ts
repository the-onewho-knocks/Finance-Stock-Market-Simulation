export class SSEConnection {
  private eventSource: EventSource | null = null

  connect(url: string, onMessage: (data: unknown) => void) {
    this.disconnect()
    this.eventSource = new EventSource(url)
    this.eventSource.onmessage = (event) => {
      try {
        onMessage(JSON.parse(event.data))
      } catch {
        onMessage(event.data)
      }
    }
  }

  disconnect() {
    this.eventSource?.close()
    this.eventSource = null
  }
}