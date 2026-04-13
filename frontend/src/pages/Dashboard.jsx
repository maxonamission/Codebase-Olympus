import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const navigate = useNavigate()

  function handleLogout() {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div className="page">
      <h1>Dashboard</h1>
      <p>Welkom bij Gymnasium Classica.</p>
      <button onClick={handleLogout}>Uitloggen</button>
    </div>
  )
}
