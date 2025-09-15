import './App.css'
import PersonalityRadarChart from './components/RadarChart'
import profileImage from './assets/defaultProfileImg.png'

function App() {
  return (
    <>
      <header>
        <h1>Spotify Personality Analyzer</h1>
        <p>Discover your music personality through your Spotify listening habits</p>
      </header>
      
      <div className="profile-bar">
        <div className="profile-info">
          <div className="profile-image">
            <img src={profileImage} alt="Profile" />
          </div>
          <span className="username">John Doe</span>
        </div>
        <button className="connect-btn">Connect to Spotify</button>
      </div>
      
      <nav className="navbar">
        <ul>
          <li><a href="#songs">Songs</a></li>
          <li><a href="#stats">Stats</a></li>
          <li><a href="#charts">Charts</a></li>
        </ul>
      </nav>
      
      <main>        
        <div className="chart-section">
          <PersonalityRadarChart />
        </div>
      </main>
      
      <footer>
        <p>&copy; 2024 Spotify Personality Analyzer</p>
      </footer>
    </>
  )
}

export default App
