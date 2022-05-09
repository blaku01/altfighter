import '../styles/globals.css'
import Navbar from '../components/navbar'
import Image from 'next/image'

function MyApp({ Component, pageProps }) {
  return (
    <>
      <div className='grid grid-cols-7 h-full w-full'>
        <Navbar/>
        <Component {...pageProps} />
        
      </div>
      <Image
        src='/bg.jpg'
        layout='fill'
        className="w-full h-full bg-no-repeat bg-cover bg-left"
        style={{ zIndex: -1 }}
      />
    </>
  )
}

export default MyApp

