import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Header from '../Header.jsx';

const MockHeader = () => (
  <BrowserRouter>
    <Header />
  </BrowserRouter>
);

describe('Header', () => {
  test('renders the app title', () => {
    render(<MockHeader />);
    const titleElement = screen.getByText(/Bitcoin Smart Contract Agent/i);
    expect(titleElement).toBeInTheDocument();
  });
});