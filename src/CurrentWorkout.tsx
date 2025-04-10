import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import WorkoutChecklist, { WorkoutChecklistProps } from "./WorkoutChecklist";
import WorkoutCard, { WorkoutCardProps } from "./WorkoutCard";
import colors from "./colors";

export default function CurrentWorkout() {
  const [currentWorkout, setCurrentWorkout] = useState<WorkoutChecklistProps[]>(
    []
  );
  const location = useLocation();
  const workouts: WorkoutChecklistProps[] = location.state?.workouts || [];
  const prompt: string = location.state?.prompt;

  function handleDoneBtn(id: number) {
    setCurrentWorkout((prev) =>
      prev.map((workout) => {
        if (workout.id === id) {
          console.log("✅ Marking complete:", id);
          return {
            ...workout,
            complete: true,
          };
        }
        return workout;
      })
    );
  }

  function handleDiscard(id: number) {
    const withoutDiscarded = currentWorkout.filter(
      (workout) => workout.id !== id
    );
    setCurrentWorkout(withoutDiscarded);
  }

  useEffect(() => {
    if (currentWorkout.length === 0 && workouts.length > 0) {
      setCurrentWorkout(
        workouts.map((workout) => ({
          ...workout,
          complete: false,
        }))
      );
    }
  }, [workouts]);

  return (
    <div className="generatedworkoutswidth">
      <h2 className="carddiv promptdiv">•• {prompt} ••</h2>
      <div className="exdiv">
        {currentWorkout
          .filter((workout) => workout.complete === false)
          .map((workout: WorkoutChecklistProps, index) => (
            <WorkoutChecklist
              key={`incomplete-${workout.id}`}
              id={workout.id}
              name={workout.name}
              equipment={workout.equipment}
              targeted_muscles={workout.targeted_muscles}
              sets={workout.sets}
              reps={workout.reps}
              className={"generatedworkout"}
              complete={workout.complete}
              style={{
                borderLeft: `2px solid ${colors[index % colors.length]}`,
                borderBottom: `2px solid ${colors[index % colors.length]}`,
              }}
              stylecolor={`${colors[index % colors.length]}`}
              onDone={() => {
                if (workout.id !== undefined) {
                  console.log("Clicked done for:", workout.id);
                  handleDoneBtn(workout.id);
                }
              }}
              onDiscard={() => {
                if (workout.id !== undefined) {
                  console.log("Clicked done for:", workout.id);
                  handleDiscard(workout.id);
                }
              }}
            />
          ))}
        <h2 className="carddiv promptdiv">•• Completed exercises ••</h2>
        {currentWorkout
          .filter((workout) => workout.complete === true)
          .map((workout: WorkoutCardProps) => (
            <WorkoutCard
              key={`complete-${workout.id}`}
              id={workout.id}
              name={workout.name}
              equipment={workout.equipment}
              targeted_muscles={workout.targeted_muscles}
              sets={workout.sets}
              reps={workout.reps}
              className={"generatedworkout"}
              complete={workout.complete}
              style={{
                borderLeft: `2px solid #2a2a2a`,
                borderBottom: `2px solid #2a2a2a`,
              }}
              stylecolor={`#cfcfcf`}
            />
          ))}
      </div>
    </div>
  );
}
