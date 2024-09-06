from typing import List
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String)
    tema_texto: Mapped[str] = mapped_column(Text)
    pregunta_id: Mapped[str] = mapped_column(String)
    pregunta_fecha_creacion: Mapped[str] = mapped_column(String)
    pregunta_texto: Mapped[str] = mapped_column(Text)
    respuesta_fecha_actualizacion: Mapped[str] = mapped_column(String)
    respuesta_texto: Mapped[str] = mapped_column(Text)
    embedding: Mapped[List[float]] = mapped_column(Vector(384))  # Usando Vector de pgvector

    tema_links: Mapped[List["TemaLink"]] = relationship(back_populates="document")
    respuesta_links: Mapped[List["RespuestaLink"]] = relationship(back_populates="document")
    preguntas_relacionadas: Mapped[List["PreguntaRelacionada"]] = relationship(back_populates="document")

class TemaLink(Base):
    __tablename__ = "tema_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    texto: Mapped[str] = mapped_column(Text)
    href: Mapped[str] = mapped_column(String)

    document: Mapped["Document"] = relationship(back_populates="tema_links")

class RespuestaLink(Base):
    __tablename__ = "respuesta_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    texto: Mapped[str] = mapped_column(Text)
    href: Mapped[str] = mapped_column(String)

    document: Mapped["Document"] = relationship(back_populates="respuesta_links")

class PreguntaRelacionada(Base):
    __tablename__ = "preguntas_relacionadas"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    texto: Mapped[str] = mapped_column(Text)
    href: Mapped[str] = mapped_column(String)

    document: Mapped["Document"] = relationship(back_populates="preguntas_relacionadas")
    