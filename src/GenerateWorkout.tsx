import WorkoutLibrary from "./WorkoutLibrary";
import React from "react";
import WorkoutCard from "./WorkoutCard";

interface GenerateWorkoutProps {
  name: string;
}

export default function GenerateWorkout(props: GenerateWorkoutProps) {
  const [upperBodyFilter, setUpperBodyFilter] = React.useState(false);
  const [lowerBodyFilter, setLowerBodyFilter] = React.useState(false);
  const [fullBodyFilter, setFullBodyFilter] = React.useState(false);
  const [coreFilter, setCoreFilter] = React.useState(false);
  const [mobilityFilter, setMobilityFilter] = React.useState(false);
  const [beginnerFilter, setBeginnerFilter] = React.useState(true);
  const [intermediateFilter, setIntermediateFilter] = React.useState(false);
  const [advancedFilter, setAdvancedFilter] = React.useState(false);

  const activeFilters = {
    "Upper Body": upperBodyFilter,
    Legs: lowerBodyFilter,
    "Full Body": fullBodyFilter,
    Core: coreFilter,
    Mobility: mobilityFilter,
    Beginner: beginnerFilter,
    Intermediate: intermediateFilter,
    Advanced: advancedFilter,
  };

  const filteredWorkout = () => {
    const categoriedWorkout = WorkoutLibrary.filter((item) => {
      return Object.entries(activeFilters).some(
        ([key, value]) => value && item.category === key
      );
    });

    const difficultyFiltered = categoriedWorkout.filter((item) => {
      return Object.entries(activeFilters).some(
        ([key, value]) => value && item.difficulty === key
      );
    });
    return categoriedWorkout && difficultyFiltered;
  };

  return (
    <>
      <h1>Hello, {props.name}</h1>
      <h2>What would you like to do today?</h2>
      <div>
        <button
          onClick={() => {
            setLowerBodyFilter(false);
            setCoreFilter(false);
            setFullBodyFilter(false);
            setMobilityFilter(false);
            setUpperBodyFilter(true);
          }}
        >
          Upper Body
        </button>
        <button
          onClick={() => {
            setLowerBodyFilter(true);
            setCoreFilter(false);
            setFullBodyFilter(false);
            setMobilityFilter(false);
            setUpperBodyFilter(false);
          }}
        >
          Lower Body
        </button>
        <button
          onClick={() => {
            setLowerBodyFilter(false);
            setCoreFilter(false);
            setFullBodyFilter(true);
            setMobilityFilter(false);
            setUpperBodyFilter(false);
          }}
        >
          Full Body
        </button>
        <button
          onClick={() => {
            setLowerBodyFilter(false);
            setCoreFilter(true);
            setFullBodyFilter(false);
            setMobilityFilter(false);
            setUpperBodyFilter(false);
          }}
        >
          Core
        </button>
        <button
          onClick={() => {
            setLowerBodyFilter(false);
            setCoreFilter(false);
            setFullBodyFilter(false);
            setMobilityFilter(true);
            setUpperBodyFilter(false);
          }}
        >
          Mobility
        </button>
      </div>
      <div>
        <button
          onClick={() => {
            setBeginnerFilter(true);
            setIntermediateFilter(false);
            setAdvancedFilter(false);
          }}
        >
          Beginner
        </button>
        <button
          onClick={() => {
            setBeginnerFilter(false);
            setIntermediateFilter(true);
            setAdvancedFilter(false);
          }}
        >
          Intermediate
        </button>
        <button
          onClick={() => {
            setBeginnerFilter(false);
            setIntermediateFilter(false);
            setAdvancedFilter(true);
          }}
        >
          Advanced
        </button>
      </div>
      <div>
        {filteredWorkout().map((item) =>
          item.workouts.map((workout, workoutIndex) => (
            <WorkoutCard
              key={`${workout.name}-${workoutIndex}`}
              name={workout.name}
              sets={workout.sets}
              reps={workout.sets}
            />
          ))
        )}
      </div>
    </>
  );
}
