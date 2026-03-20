import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using Http;

@service(#{
  title: "Library Management Service",
})
@server("http://localhost:8080/api", "Cổng API Flask")
namespace Library;

// Model thuần túy - chỉ chứa dữ liệu sách
model Book {
  id?: int32;
  title: string;
  author: string;
}

@route("/books")
interface Books {
  @get list(): Book[];
  
  @post create(@body book: Book): {
    @statusCode statusCode: 201;
    @body createdBook: Book;
  };

  @route("/{id}")
  @get getBook(@path id: int32): Book | { @statusCode statusCode: 404 };

  @route("/{id}")
  @delete deleteBook(@path id: int32): { @statusCode statusCode: 204 };
}