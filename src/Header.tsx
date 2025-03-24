interface HeaderProps {
  color: string;
  headingRef: React.RefObject<HTMLHeadingElement | null>;
}

export default function Header({ color, headingRef }: HeaderProps) {
  return (
    <>
      <div className="workoutimgcontainer">
        <img
          className="workoutimg"
          src="https://images.unsplash.com/photo-1557330359-ffb0deed6163?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          alt="workout equipment"
        />
      </div>

      {
        <div className="notgeneratedcontainer">
          <h1 ref={headingRef} style={{ color }}>
            Time for gains!
          </h1>
          <p className="greet">What would you like to do today?</p>
        </div>
      }
    </>
  );
}
