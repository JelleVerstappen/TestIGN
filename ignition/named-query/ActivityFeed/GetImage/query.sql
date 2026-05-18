select
	cast(ImageBlob as image) as Image
from
	AFComments
where
	CommentID = :commentID