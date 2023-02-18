import {render, screen} from "@testing-library/react";

import App from "./App";

test("renders Hitas heading", () => {
    render(<App />);
    const linkElement = screen.getByText(/Hitas/i);
    expect(linkElement).toBeInTheDocument();
});
