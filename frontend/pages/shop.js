import { useState, useEffect } from 'react';
import UserComponent from '../components/userComponent'

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
      <div className={`h-[90%] w-[45vw] my-[5vh] flex items-center justify-center border`} style={{ zIndex: 1 }}>
        <div className='h-full w-[90%] flex flex-col border'>
          <div className='h-[60%] w-full border'></div>
          <div className='h-[40%] w-full flex flex-wrap items-center justify-center  border'>
            {data.shop.map((item, index) => {
              return(
              <div className="w-[25%] h-[40%] mx-[3%] border">
                {item.id} {item.name} {item.price}
              </div>
            )})}
          </div>
        </div>
      </div>
    </>
  )
}


export default Shop;

