import { useNavigate } from "react-router-dom";

interface ButtonProps {
  color: string;
}

export default function ChoiceButtons({ color }: ButtonProps) {
  const navigate = useNavigate();
  return (
    <div className="notgeneratedcontainer">
      <form>
        <input type="text" />
        <button type="submit" style={{ backgroundColor: color }}>
          Ask for a workout
        </button>
        <p> - or - </p>
        <button
          onClick={(e) => {
            e.preventDefault();
            navigate("/browse");
          }}
          style={{ backgroundColor: color }}
        >
          Browse workout history
        </button>
      </form>
    </div>
  );
}
