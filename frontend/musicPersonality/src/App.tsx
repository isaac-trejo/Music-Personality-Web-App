import './App.css'
import PersonalityRadarChart from './components/RadarChart'
import profileImage from './assets/defaultProfileImg.png'

function App() {
  return (
    <>
      <header>
        <div className="profile-bar">
        <div className="profile-info">
          <div className="profile-image">
            <img src={profileImage} alt="Profile" />
          </div>
          <span className="username">John Doe</span>
        </div>
        <button className="connect-btn">Connect to Spotify</button>
      </div>
      </header>
      
      <nav className="navbar">
        <ul>
          <li><a href="#songs">Songs</a></li>
          <li><a href="#stats">Stats</a></li>
          <li><a href="#charts">Charts</a></li>
        </ul>
      </nav>
      
      <h1>Spotify Personality Analyzer</h1>
      <p>Discover your personality through your Spotify listening habits</p>

      <main>        
        <div className="chart-section">
          <PersonalityRadarChart />
        </div>
      </main>
      
      <footer>
        {/* TODO: Add extra info */}
      </footer>
    </>
  )
}

export default App
