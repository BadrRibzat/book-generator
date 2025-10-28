# Book Generator Frontend

Vue 3 + TypeScript + Vite frontend for the Book Generator application.

## Tech Stack

- **Vue 3.5+**: Composition API with `<script setup>`
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool with HMR
- **Vue Router 4**: Client-side routing
- **Pinia**: State management
- **Axios**: HTTP client
- **Tailwind CSS**: Utility-first styling
- **Font Awesome**: Icon library

## Project Structure

```
src/
├── views/           # Page components
│   ├── Auth/        # Authentication views
│   │   ├── SignUp.vue
│   │   └── SignIn.vue
│   ├── Books/       # Book management views
│   │   ├── List.vue
│   │   ├── Create.vue
│   │   ├── Details.vue
│   │   └── SelectCover.vue
│   └── Profile.vue  # User profile
├── stores/          # Pinia stores
│   ├── auth.ts      # Authentication state
│   └── books.ts     # Books state
├── services/        # API services
│   └── api.ts       # Axios instance
├── router/          # Vue Router config
│   └── index.ts     # Routes & guards
├── types/           # TypeScript types
│   └── index.ts     # API types
├── utils/           # Utility functions
│   └── helpers.ts   # Common helpers
├── components/      # Reusable components
├── assets/          # Static assets
├── App.vue          # Root component
├── main.ts          # App entry point
└── style.css        # Global styles
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Django backend running on http://127.0.0.1:8000

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start dev server (http://localhost:5173)
npm run dev
```

### Build

```bash
## E2E Browser Tests (Playwright)

We use Playwright for real browser UI/UX tests.

### Install Playwright (one-time)

```bash
npm install
npx playwright install  # installs browsers
```

If you're on Linux and missing system dependencies, use:

```bash
npx playwright install --with-deps
```

### Run tests

```bash
npm run test:e2e          # headless
npm run test:e2e:headed   # visible browser
```

By default, tests will start the Vite dev server on http://localhost:5173 and reuse it if already running.
# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
# API base URL (optional, defaults to http://127.0.0.1:8000/api)
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Features

### Authentication
- **Sign Up**: Create new account with username, email, password
- **Sign In**: Login with username and password
- **Session-based auth**: Uses cookies (no JWT)
- **Profile**: View user details and sign out
- **Route guards**: Protected routes redirect to sign in

### Book Management
- **Create Book**: Select domain, niche, and page length
- **Book List**: View all books with status indicators
- **Book Details**: Track generation progress
- **Select Cover**: Choose from 3 generated covers
- **Download**: Get final PDF when ready
- **Delete**: Remove unwanted books

### Book Categories

**5 Domains with 15 Trending Niches:**

1. **Language & Kids**
   - AI Learning Stories
   - Multilingual Coloring Books
   - Kids Mindfulness Journals

2. **Technology & AI**
   - AI Ethics & Responsibility
   - No-Code Development Guides
   - Smart Home DIY

3. **Nutrition & Wellness**
   - Specialty Diet Cookbooks
   - Plant-Based Cooking
   - Nutrition for Mental Health

4. **Meditation & Mindfulness**
   - Mindfulness for Anxiety
   - Sleep Meditation Guides
   - Gratitude Journals

5. **Home Workout & Fitness**
   - Equipment-Free Workouts
   - Yoga for Remote Workers
   - Mobility Training

## API Integration

The frontend communicates with the Django REST API:

- **Base URL**: `http://127.0.0.1:8000/api`
- **Auth**: Session-based (cookies)
- **Endpoints**:
  - `POST /users/register/` - Sign up
  - `POST /users/login/` - Sign in
  - `POST /users/logout/` - Sign out
  - `GET /users/me/` - Current user
  - `GET /books/` - List books
  - `POST /books/` - Create book
  - `GET /books/:id/` - Book details
  - `POST /books/:id/select-cover/` - Select cover
  - `DELETE /books/:id/` - Delete book

## State Management

### Auth Store (`stores/auth.ts`)
- User state and authentication
- `signUp()`, `signIn()`, `signOut()`, `checkAuth()`
- Auto-checks auth on app load

### Books Store (`stores/books.ts`)
- Books list and current book
- `createBook()`, `fetchBooks()`, `fetchBook()`
- `selectCover()`, `deleteBook()`

## Styling

- **Tailwind CSS**: Utility-first classes
- **Custom theme**: Primary blue colors (50-900 shades)
- **Responsive**: Mobile-first design
- **Font**: Inter font family

## TypeScript Types

All API types are defined in `types/index.ts`:
- `User`, `UserLogin`, `UserRegistration`
- `Book`, `BookCreate`, `BookStatus`
- `Cover`, `CoverSelect`, `CoverStyle`
- `Domain`, `SubNiche`, `PageLength`

## Development Tips

1. **Hot reload**: Changes auto-reload in dev mode
2. **Type checking**: TypeScript catches errors at compile time
3. **Vue DevTools**: Install browser extension for debugging
4. **API errors**: Check browser console and Network tab
5. **CORS**: Backend must allow frontend origin

## Troubleshooting

### "Cannot connect to backend"
- Ensure Django server is running on port 8000
- Check CORS settings in Django
- Verify `withCredentials: true` in axios config

### "Authentication fails"
- Check Django session settings
- Verify cookies are being set
- Check `SESSION_COOKIE_SAMESITE` in Django

### "Build errors"
- Run `npm install` to update dependencies
- Check TypeScript errors with `npm run build`
- Ensure all imports are correct

## License

MIT

