import { useState, useEffect } from 'react';


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
    <div className={`h-full w-full flex items-center justify-center`} style={{ zIndex: 1 }}>
      <div className="self-center flex bg-transparent	 shadow rounded">
        <ul>{data.shop.map((item, index) => {
          return <li>{item.id} {item.name} {item.price}</li>
        })}
        </ul>
      </div>
    </div>
  )
}


export default Shop;

