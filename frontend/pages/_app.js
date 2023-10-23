import '../styles/globals.css'
import Navbar from '../components/navbar'
import Image from 'next/image'

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Image
        src='/bg.jpg'
        layout='fill'
        className="w-full h-full bg-no-repeat bg-cover bg-left"
        style={{ zIndex: -1 }}
      />
      <div className={`absolute w-full h-full flex`} style={{ zIndex: 1 }}>
        <Navbar />
        <Component {...pageProps} />

      </div>
    </>
  )
}

export default MyApp

