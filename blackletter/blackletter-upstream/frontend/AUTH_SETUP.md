# Supabase Authentication Setup

This guide will help you set up Supabase authentication for the Blackletter Systems frontend.

## Prerequisites

1. A Supabase account (sign up at https://app.supabase.com)
2. Node.js and npm installed

## Setup Instructions

### 1. Create a Supabase Project

1. Go to https://app.supabase.com
2. Click "New Project"
3. Fill in your project details
4. Wait for the project to be created

### 2. Get Your Project Credentials

1. In your Supabase dashboard, go to Settings > API
2. Copy the following values:
   - `Project URL`
   - `Project API Keys` > `anon` `public`

### 3. Configure Environment Variables

1. Create a `.env.local` file in the frontend directory
2. Add your Supabase credentials:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Install Dependencies

```bash
cd frontend
npm install
```

### 5. Run the Development Server

```bash
npm run dev
```

## Features Included

- **User Registration**: New users can create accounts with email/password
- **User Login**: Existing users can sign in
- **Protected Routes**: Navigation changes based on authentication state
- **User Profile**: Basic user metadata support (name, company)
- **Password Reset**: Foundation for password recovery (to be implemented)

## Authentication Flow

1. Users can register at `/auth/register`
2. Users can login at `/auth/login`
3. Authenticated users see different navigation options
4. Users can logout using the navigation button

## File Structure

```
frontend/
├── app/
│   ├── auth/
│   │   ├── login/page.tsx          # Login page
│   │   ├── register/page.tsx       # Registration page
│   │   └── layout.tsx              # Auth layout
│   └── layout.tsx                  # Root layout with AuthProvider
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx           # Login form component
│   │   └── RegisterForm.tsx        # Registration form component
│   ├── ui/                         # UI components (Button, Input, etc.)
│   └── Navigation.tsx              # Auth-aware navigation
├── contexts/
│   └── AuthContext.tsx             # Authentication context
├── lib/
│   ├── supabase.ts                 # Supabase configuration
│   └── utils.ts                    # Utility functions
└── .env.example                    # Environment variables template
```

## Customization

- **Styling**: The components use Tailwind CSS with the existing Blackletter color scheme
- **Validation**: Forms include basic validation and error handling
- **User Metadata**: Registration captures additional user info (name, company)
- **UI Components**: Consistent with the existing design system

## Next Steps

1. Set up your Supabase project
2. Configure authentication policies in Supabase
3. Test the registration and login flow
4. Integrate with your backend API for user-specific data

## Troubleshooting

- Ensure environment variables are correctly set
- Check Supabase project settings and authentication configuration
- Verify that email authentication is enabled in Supabase Auth settings
