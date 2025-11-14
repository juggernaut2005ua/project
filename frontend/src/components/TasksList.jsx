import React from 'react'

export default function TasksList({tasks}){
  if(!tasks || tasks.length===0) return <p>Задач не найдено.</p>
  return (
    <div className="tasks">
      {tasks.map(t => (
        <div key={t.id} className="task">
          <h3>{t.name} <small>({t.get_direction_display || t.direction})</small></h3>
          <p>{t.description}</p>
          <div className="meta">Статус: <strong>{t.status}</strong> — Создано: {new Date(t.created_at).toLocaleString()}</div>
        </div>
      ))}
    </div>
  )
}
