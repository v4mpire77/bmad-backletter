# Blackletter Frontend

This is the frontend application for the Blackletter GDPR Processor, built with Next.js.

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Demo Mode

This application includes a demo mode that uses mock data to showcase the product flow without requiring a backend.

To enable demo mode:

1. Create a `.env.local` file in the root of the frontend directory (this directory)
2. Add the following line to the file:

```
NEXT_PUBLIC_USE_MOCKS=1
```

With demo mode enabled, you can:
- View a seeded contract on the dashboard
- Navigate to the findings page to see mock findings
- Use the export dialog to simulate exporting a report
- View the reports page to see mock export history

To disable demo mode, either:
- Remove the `NEXT_PUBLIC_USE_MOCKS` variable from `.env.local`
- Set it to `0`:

```
NEXT_PUBLIC_USE_MOCKS=0
```

When demo mode is disabled, the application will attempt to connect to the real API endpoints.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!