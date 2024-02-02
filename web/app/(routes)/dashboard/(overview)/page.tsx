import getServerUser from '@/app/lib/firebase/getServerUser'

export default async function App() {
  const user = await getServerUser()
  const formattedString = JSON.stringify(user, null, "\t");

  return (
    <div className='mx-auto max-w-4xl my-32 '>
      <h1 className='text-3xl mb-8'>Welcome to the protected area of the app</h1>
      <div className="relative bg-gray-800 p-4 rounded-md shadow-md overflow-x-auto">
        <pre  className="text-sm text-white font-mono">
          <code>{formattedString}</code>
        </pre>
      </div>
    </div>
  )
}
