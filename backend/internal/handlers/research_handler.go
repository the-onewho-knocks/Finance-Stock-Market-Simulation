package handler

import (
	"net/http"
	"net/http/httputil"
	"net/url"
)

type ResearchHandler struct {
	proxy *httputil.ReverseProxy
}

func NewResearchHandler(targetURL string) *ResearchHandler {
	target, _ := url.Parse(targetURL)
	return &ResearchHandler{
		proxy: httputil.NewSingleHostReverseProxy(target),
	}
}

func (h *ResearchHandler) Proxy(w http.ResponseWriter, r *http.Request) {
	h.proxy.ServeHTTP(w, r)
}
