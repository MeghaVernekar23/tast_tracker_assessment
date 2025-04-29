export const Datatable = ({ columns, data, actions = [] }) => {
  return (
    <div className="table-responsive">
      <table className="table table-striped table-bordered ">
        <thead className="table-dark">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="fw-bold">
                {col.label}
              </th>
            ))}
            {actions.length > 0 && <th className="fw-bold">Actions</th>}
          </tr>
        </thead>
        <tbody>
          {data.length > 0 ? (
            data.map((row, index) => (
              <tr key={index}>
                {columns.map((col) => (
                  <td key={col.key} className="align-middle">
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
                {actions.length > 0 && (
                  <td className="text-end align-middle">
                    {actions.map((action, idx) => (
                      <i
                        key={idx}
                        className={`bi ${action.icon} me-2`}
                        title={action.label}
                        onClick={() => action.onClick(row)}
                        role="button"
                      />
                    ))}
                  </td>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={columns.length + (actions.length > 0 ? 1 : 0)}
                className="text-center text-muted py-3"
              >
                No data available.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};
