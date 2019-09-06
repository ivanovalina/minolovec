<h1>Choose field</h1>
<br />
% if table.is_gameover:
<h2>Game over!</h2>
% end
% if table.is_winner():
<h2>WIN!</h2>
% end
<form action='/click' method='POST'>
% for i in range(table.x_size):
%   for j in range(table.y_size):
%     if table.xy_value(i,j) == -2:
        <button type='submit' name='button' value='{{ i }},{{ j }}'></button>
%     elif table.xy_value(i,j) == -1:
        <button type='button'>M</button>
%     elif table.xy_value(i,j) == 0:
        <button type='button'>E</button>
%     else:
        <button type='button'>{{ table.xy_value(i,j) }}</button> 
<!--        <button type='button'>X</button>  -->
%     end
%   end
  <br />

% end
</form>
<a href = '/'> New game </a>

