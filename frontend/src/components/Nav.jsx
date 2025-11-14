import React from 'react'

export default function Nav(){
  return (
    <nav className="topnav">
      <div className="container">
        <a className="brand" href="#">Интеграционная панель</a>
        <div className="right">API: <code>{import.meta.env.VITE_API_BASE_URL || '/api'}</code></div>
      </div>
    </nav>
  )
}
