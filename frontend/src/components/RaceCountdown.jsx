import { getNextRace } from "../services/api";
import React, { useState, useEffect, use } from 'react'
import { differenceInSeconds, formatDistanceToNow } from 'date-fns';

const options = {
        weekday: 'short',
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short' // This adds "PST", "GMT", etc.
        }

export default function RaceCountdown() {
    const [raceData, setRaceData] = useState(null)
    const [timeLeft, setTimeLeft] = useState("")

    // This runs once when component loads
    useEffect(() => {
        getRaceData()
    }, [])

    const getRaceData  = async () => {
        try {
            const data = await getNextRace()
            setRaceData(data)
        } catch(error) {
            console.error("Error getting data from API", error)
        }
    }

    // This runs every second to update countdown
    useEffect(() => {
        if (!raceData) {
            return
        }

        const timer = setInterval(() => {
            const now = new Date()
            const dateOfRace = new Date(raceData.race_date)
            const secondsRemaining = differenceInSeconds(dateOfRace, now)

            secondsRemaining <= 0 
            ? 
                setTimeLeft("Race has started! 🏁") 
            : 
                setTimeLeft(formatTimeLeft(secondsRemaining))
        }, 1000)

        return () => clearInterval(timer)
    }, [raceData])

    // Helper function to format seconds into "2d 14h 32m 15s"

    const formatTimeLeft = seconds => {
        const days = Math.floor(seconds / 86400)
        const hours = Math.floor((seconds % 86400) / 3600) 
        const minutes = Math.floor((seconds % 3600) / 60)
        const secs = seconds % 60

        return `${days} days ${hours} hours ${minutes} minutes ${secs} seconds`
    }


    return (
        <>
            <div className="race-countdown-container">
                <AnimatedBackgroundEffects />
                <div className="main-content">
                    {raceData 
                    ? 
                        (
                            <>
                                <Header raceData={raceData}/>
                                <Countdown timeLeft={timeLeft}/>
                                <TrackInfo />
                                <RaceSessionsBlock sessions={raceData.sessions}/>
                            </>
                        ) 
                    : 
                        (
                            <LoadingNextRace />
                        )
                    }
                </div>
            </div>
        </>
    )
};

function AnimatedBackgroundEffects() {
    return (
        <>
            {/* Animated background elements */}
            <div className="background-orb background-orb-1" />
            <div className="background-orb background-orb-2" />
            <div className="background-orb background-orb-3" />
        </>
    )
}

function Header({raceData}) {
    return (
        <>
            {/* Header Section */}
            <div className="race-header">
                <h1 className="race-title">
                {raceData.race_name}
                </h1>
            </div>
        </>
    )
}

function Countdown({timeLeft}) {
    return (
        <>
            {/* Countdown Section */}
            <div className="countdown-container">
                <h2 className="countdown-title">Next Race In</h2>
                <div className="countdown-timer">
                {timeLeft}
                </div>
                <div className="countdown-bar" />
            </div>
        </>
    )
}

function TrackInfo({
        trackName = "Baku City Circuit",
        length = "306.049km",
        laps = "51",
        corners = "20",
        lapRecord = "1:43.009",
        lapRecordDriver="Charles Leclerc",
        lapRecordYear=2019,
        firstGP = "2016",
        trackImageUrl = "http://localhost:8000/api/track-image/Azerbaijan"
}) {
    return (
        <>
<div className="track-info-container">
      <div className="track-content">
        {/* Track Image */}
        <div className="track-image-wrapper">
          <img 
            src={trackImageUrl}
            alt={`${trackName} track layout`}
            className="track-image"
          />
        </div>

        {/* Track Info */}
        <div className="track-details">
          <h3 className="track-name">
            {trackName}
          </h3>


          {/* Stats Row */}
          <div className="track-stats">
            <div className="stat-item">
              <div className="stat-label">Length</div>
              <div className="stat-value">{length}</div>
            </div>

            <div className="stat-item">
              <div className="stat-label">Laps</div>
              <div className="stat-value">{laps}</div>
            </div>

            <div className="stat-item">
              <div className="stat-label">Corners</div>
              <div className="stat-value">{corners}</div>
            </div>

            <div className="stat-item stat-item-highlighted">
              <div className="stat-label">Record</div>
              <div className="stat-value">{lapRecord}</div>
              <div className="sub-stat-value">{lapRecordDriver}({lapRecordYear})</div>

            </div>

            <div className="stat-item">
              <div className="stat-label">First GP</div>
              <div className="stat-value">{firstGP}</div>
            </div>
          </div>
        </div>
      </div>
    </div>  
        </>
    )
}

function RaceSession({data}) {
    const classes = {
        'Practice 1': 'session-practice-1',
        'Practice 2': 'session-practice-2',
        'Practice 3': 'session-practice-3',
        'Qualifying': 'session-qualifying',
        'Grand Prix': 'session-race'
    };

    const colors = {
        'Practice 1': '#3b82f6',
        'Practice 2': '#3b82f6',
        'Practice 3': '#8b5cf6',
        'Qualifying': '#f59e0b',
        'Race': '#ef4444'
    };
    const [isHovered, setIsHovered] = useState(false);

    const getSessionClass = (sessionName) => {
        return classes[sessionName] || 'session-default';
  };

    const getIndicatorColor = (sessionName) => {
        return colors[sessionName] || '#6b7280';
    };

    return (
        <>
            <div 
            className="race-block"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            >
            <div className="race-block-circle-container">
                <div className={`race-block-circle ${getSessionClass(data.name)}`}>
                <div>
                    <div>{data.name.split(' ')[0]}</div>
                    {data.name.includes(' ') && (
                    <div>{data.name.split(' ')[1]}</div>
                    )}
                </div>
                
                {/* Animated ring */}
                <div className="race-block-ring" />
                </div>
                
                {/* Pulsing dot indicator */}
                <div 
                className="race-block-indicator"
                style={{ backgroundColor: getIndicatorColor(data.name) }}
                >
                <div 
                    className="race-block-indicator-ping"
                    style={{ backgroundColor: getIndicatorColor(data.name) }}
                />
                </div>
            </div>
            
            <div className="race-block-datetime">
                <div>{data.datetime}</div>
            </div>
            </div>
        </>
    )
}

function RaceSessionsBlock({sessions}) {
    return (
        <>
            {/* Sessions Section */}
            <div className="sessions-section">
                <h3 className="sessions-title">
                    Race Weekend Sessions
                </h3>
                <div className="sessions-container">
                    {sessions.map((session) => (
                        <RaceSession 
                            key={session.name}
                            data={{
                                ...session,
                                datetime: new Date(session.datetime).toLocaleDateString("en-US", options)
                            }} 
                        />
                ))}
                </div>
            </div>
        </>
    )
}

function LoadingNextRace() {
    return  (
        <>
            <div className="loading-container">
                <div className="loading-content">
                    <div className="loading-spinner" />
                    <div className="loading-text">Loading next race...</div>
                </div>
            </div>
        </>
    )
} 

