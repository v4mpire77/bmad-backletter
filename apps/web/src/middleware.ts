import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  // Redirect disabled to show landing page
  // if (req.nextUrl.pathname === '/') {
  //   return NextResponse.redirect(new URL('/upload', req.url));
  // }
}

export const config = { matcher: ['/'] };
