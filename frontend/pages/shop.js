import { useState, useEffect } from 'react';
import UserComponent from '../components/userComponent'
import Image from 'next/image'

function Shop(res, req) {
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(false)
  useEffect(() => {
    setLoading(true)
    fetch('/api/shop/')
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
  }, [])
  if (isLoading) return <p>Loading...</p>
  if (!data) return <p>No profile data</p>
  return (
    <>
      <UserComponent />
      <div className={`h-[90%] w-[45vw] my-[5vh] flex items-center justify-center`} style={{ zIndex: 1 }}>
        <div className='h-full w-[90%] flex flex-col'>
          <div className='relative h-[60%] w-full'>
            <Image
              src="/weapon-shop.png"
              alt="Picture of the author"
              layout='fill'
            />
          </div>
          <div className='h-[40%] w-full flex flex-wrap items-center justify-center'>
            {data.shop.map((item, index) => {
              return (
                <div key={index} className={`group w-[25%] h-[40%] mx-[3%] border`}>
                  <div className='relative h-[100%] w-[100%] flex items-center justify-center'>
                    <div className='relative h-[70%] w-[70%] flex -teims-center justify-center'>
                      <Image
                        src="/icons/sword.webp"
                        alt="Picture of the author"
                        layout='fill'
                      />
                    </div>
                    <div className={`absolute w-[100%] h-[100%] -top-[100%] flex flex-col items-center justify-center invisible group-hover:visible bg-slate-500`}>
                      <h3 className='uppercase'>{item.name}</h3>
                      {item.strength != 0 ? <p>strength: {item.strength}</p> : <></>}
                      {item.agility != 0 ? <p>agility: {item.agility}</p> : <></>}
                      {item.vitality != 0 ? <p>vitality: {item.vitality}</p> : <></>}
                      {item.luck != 0 ? <p>luck: {item.luck}</p> : <></>}
                      {item.damage != 0 ? <p>damage: {item.damage}</p> : <></>}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </>
  )
}


export default Shop;
