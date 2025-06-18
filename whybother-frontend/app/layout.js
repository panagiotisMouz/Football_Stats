// app/layout.js
import './globals.css';
import Navbar from "../components/Navbar";

export const metadata = {
  title: 'WhyBother',
  description: 'Football Stats Explorer',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <title>{metadata.title}</title>
        <meta name="description" content={metadata.description} />
      </head>
      <body style={{ margin: 0, fontFamily: 'sans-serif', backgroundColor: '#121212', color: '#f5f5f5' }}>
        <Navbar />
        <main style={{ minHeight: '90vh' }}>{children}</main>
        <footer style={{ textAlign: 'center', padding: '1rem', backgroundColor: '#1e1e1e', color: '#ccc' }}>
          © {new Date().getFullYear()} WhyBother — Football Stats Explorer
        </footer>
      </body>
    </html>
  );
}
