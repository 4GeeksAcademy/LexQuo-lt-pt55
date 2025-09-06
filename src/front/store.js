export const initialStore = () => {
  return {
    message: null,
    courtfiles: [],
    todos: [],
  };
};

export default function storeReducer(store, action = {}) {
  switch (action.type) {
    case "set_hello":
      return {
        ...store,
        message: action.payload,
      };

    case "add_task":
      const { id, color } = action.payload;

      return {
        ...store,
        todos: store.todos.map((todo) =>
          todo.id === id ? { ...todo, background: color } : todo
        ),
      };

    case "SET_COURTFILES":
      return { ...store, courtfiles: action.payload };
    case "ADD_COURTFILE":
      return { ...store, courtfiles: [...store.courtfiles, action.payload] };
    case "DELETE_COURTFILE":
      return {
        ...store,
        courtfiles: store.courtfiles.filter((cf) => cf.id !== action.payload),
      };
    case "UPDATE_COURTFILE":
      return {
        ...store,
        courtfiles: store.courtfiles.map((cf) =>
          cf.id === action.payload.id ? action.payload : cf
        ),
      };
    default:
      throw Error("Unknown action.");
  }
}
