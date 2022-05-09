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

    <div className="w-full max-w-xs fixed">
      <ul>{data.shop.map((item, index) => {
        return <li>{item.id} {item.name} {item.price}</li>
      })}
      </ul>
    </div>
  )
}


export default Shop;

