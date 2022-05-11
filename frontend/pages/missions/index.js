import { useState, useEffect } from 'react';
import Link from 'next/link'


function Missions(res, req) {
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(false)
  useEffect(() => {
    setLoading(true)
    fetch('/api/missions/')
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
  }, [])
  if (isLoading) return <p>Loading...</p>
  if (!data) return <p>No profile data</p>
  return (

    <div className={`col-span-6 w-[100%] flex items-center justify-center`} style={{ zIndex: 1 }}>
      <div className='w-[50%] h-[50%] flex justify-around	 border'>
        {data.missions.map((mission, index) => {
          return (
            <Link href={`/missions/${mission.id}`}>
              <div key={index} className='w-30% flex flex-col justify-around'>

                <div>
                  <p>{mission.name}</p>
                </div>
                <div>
                  <p>{mission.time}</p>
                </div>
                <div>
                  <p>currency: {mission.currency}</p>
                </div>
                <div>
                  <p>exp: {mission.exp}</p>
                </div>
              </div>
            </Link>

          )
        })}
      </div>

    </div>
  )
}


export default Missions;

