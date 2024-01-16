import Link from 'next/link';
// import NavLinks from '@/app/ui/dashboard/nav-links';
import Logo from '@/app/ui/logo';
// import { PowerIcon } from '@heroicons/react/24/outline';

export default function SideNav() {
  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
        <Link
            className="mb-2 flex h-20 items-end justify-start rounded-md bg-blue-600 p-4 md:h-40"
            href="/"
        >
        <div className="w-32 text-white md:w-40">
            <Logo />
        </div>
      </Link>
    </div>
  );
}
